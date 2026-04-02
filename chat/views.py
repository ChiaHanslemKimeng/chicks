import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import ChatRoom, Message


def _get_or_create_room(request, visitor_name='Guest', visitor_email=''):
    """Get or create a chat room tied to this visitor's session."""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    room, created = ChatRoom.objects.get_or_create(
        session_key=session_key,
        defaults={
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
        }
    )
    # Update name/email if provided
    if not created and visitor_name and visitor_name != 'Guest':
        room.visitor_name = visitor_name
        room.visitor_email = visitor_email
        room.save(update_fields=['visitor_name', 'visitor_email'])
    return room


@csrf_exempt
@require_http_methods(["POST"])
def init_chat(request):
    """Initialize or retrieve a chat room for the visitor."""
    try:
        data = json.loads(request.body)
        name = data.get('name', 'Guest')[:100]
        email = data.get('email', '')[:254]
    except (json.JSONDecodeError, AttributeError):
        name, email = 'Guest', ''

    room = _get_or_create_room(request, name, email)
    messages = list(room.messages.values('id', 'content', 'is_from_admin', 'timestamp', 'is_read'))
    for m in messages:
        m['timestamp'] = m['timestamp'].strftime('%H:%M')

    return JsonResponse({
        'room_id': room.id,
        'visitor_name': room.visitor_name,
        'messages': messages,
    })


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Visitor sends a message."""
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    if not content:
        return JsonResponse({'error': 'Empty message'}, status=400)

    room = _get_or_create_room(request)
    msg = Message.objects.create(
        room=room,
        content=content,
        is_from_admin=False,
    )
    # Update room's last_message_at
    room.last_message_at = timezone.now()
    room.save(update_fields=['last_message_at'])

    return JsonResponse({
        'id': msg.id,
        'content': msg.content,
        'is_from_admin': False,
        'timestamp': msg.timestamp.strftime('%H:%M'),
    })


@require_http_methods(["GET"])
def poll_messages(request):
    """Long-poll: returns new messages since last_id."""
    last_id = int(request.GET.get('last_id', 0))
    room = _get_or_create_room(request)
    new_msgs = room.messages.filter(id__gt=last_id)
    # Mark admin messages as read
    new_msgs.filter(is_from_admin=True).update(is_read=True)
    data = list(new_msgs.values('id', 'content', 'is_from_admin', 'timestamp'))
    for m in data:
        m['timestamp'] = m['timestamp'].strftime('%H:%M')
    return JsonResponse({'messages': data})


# ─── Admin Views ─────────────────────────────────────────────────────────────

@staff_member_required
def admin_chat_list(request):
    """Admin: list all active conversations."""
    rooms = ChatRoom.objects.all()
    for room in rooms:
        room.unread = room.unread_admin_count()
    return render(request, 'chat/admin_list.html', {'rooms': rooms})


@staff_member_required
def admin_chat_detail(request, room_id):
    """Admin: view a conversation."""
    room = get_object_or_404(ChatRoom, id=room_id)
    # Mark visitor messages as read
    room.messages.filter(is_from_admin=False, is_read=False).update(is_read=True)
    chat_messages = room.messages.all()
    return render(request, 'chat/admin_detail.html', {'room': room, 'chat_messages': chat_messages})


@staff_member_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_reply(request, room_id):
    """Admin: send a reply to a visitor."""
    room = get_object_or_404(ChatRoom, id=room_id)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
    except (json.JSONDecodeError, AttributeError):
        content = request.POST.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'Empty message'}, status=400)

    msg = Message.objects.create(
        room=room,
        content=content,
        is_from_admin=True,
    )
    room.last_message_at = timezone.now()
    room.save(update_fields=['last_message_at'])

    return JsonResponse({
        'id': msg.id,
        'content': msg.content,
        'is_from_admin': True,
        'timestamp': msg.timestamp.strftime('%H:%M'),
        'visitor_name': room.visitor_name,
    })


@staff_member_required
@require_http_methods(["GET"])
def admin_poll(request, room_id):
    """Admin: poll for new visitor messages in a room."""
    room = get_object_or_404(ChatRoom, id=room_id)
    last_id = int(request.GET.get('last_id', 0))
    new_msgs = room.messages.filter(id__gt=last_id)
    new_msgs.filter(is_from_admin=False).update(is_read=True)
    data = list(new_msgs.values('id', 'content', 'is_from_admin', 'timestamp'))
    for m in data:
        m['timestamp'] = m['timestamp'].strftime('%H:%M')
    return JsonResponse({'messages': data})
