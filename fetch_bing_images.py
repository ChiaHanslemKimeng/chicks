import os
import django
import shutil
from django.core.files.base import ContentFile
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultry_farm.settings')
django.setup()

from fowls.models import Product, ProductImage
from bing_image_downloader import downloader
from PIL import Image
import imghdr

def run():
    print("Fixing images using Bing Image Downloader...")
    
    output_dir = "bing_downloads"
    
    for product in Product.objects.all():
        breed_n = product.breed.name if product.breed else product.name
        cat_n = product.category.name if product.category else ''
        
        search_query = f"{breed_n} {cat_n} photo realistic high quality"
        if "Coop" in product.name or "Feeder" in product.name or "Tractor" in product.name:
            search_query = f"{product.name} product photo"
        elif "Eggs" in cat_n:
            search_query = f"{product.name} food photo"
             
        print(f"\n=> Querying Bing for: {search_query}")
        
        # Download will create folder bing_downloads/<search_query>/...
        # Let's ensure it doesn't get cluttered
        search_dir = os.path.join(output_dir, search_query)
        if os.path.exists(search_dir):
            shutil.rmtree(search_dir)
            
        try:
            downloader.download(
                search_query, 
                limit=1,  
                output_dir=output_dir, 
                adult_filter_off=False, 
                force_replace=False, 
                timeout=10, 
                verbose=False
            )
            
            # Find the downloaded file
            if os.path.exists(search_dir):
                files = os.listdir(search_dir)
                if files:
                    file_path = os.path.join(search_dir, files[0])
                    
                    # Verify it is a valid image before saving
                    if imghdr.what(file_path):
                        with open(file_path, 'rb') as f:
                            image_content = f.read()
                            
                        filename = f"bing_{product.id}_{int(datetime.now().timestamp())}.jpg"
                        
                        # Save main image
                        product.thumbnail.save(filename, ContentFile(image_content), save=True)
                        
                        # Save sub image
                        product.images.all().delete()
                        sub_filename = f"bing_sub_{product.id}_{int(datetime.now().timestamp())}.jpg"
                        ProductImage.objects.create(
                            product=product,
                            image=ContentFile(image_content, name=sub_filename)
                        )
                        print("   => Saved image successfully!")
                    else:
                        print("   => Downloaded file was not a valid image format.")
                else:
                    print("   => No file found in download directory.")
            else:
                 print("   => Directory was not created by downloader.")
        except Exception as e:
            print(f"Error fetching {search_query}: {e}")
            
    # Cleanup downloads
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    print("Image fixing complete.")

if __name__ == '__main__':
    run()
