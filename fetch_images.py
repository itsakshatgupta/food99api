import requests
import cloudinary.uploader
from django.core.files.base import ContentFile
from urllib.parse import quote
from food99api.models import MenuItem

def run():
    for item in MenuItem.objects.all():
        uploaded = False

        # 1️⃣ Try with item name
        queries = [
            f"{item.name} food",
            f"{item.category.name} food",
            "Indian food" if "Indian" in item.category.name else "food"
        ]

        for q in queries:
            url = f"https://source.unsplash.com/600x400/?{quote(q)}"
            response = requests.get(url, allow_redirects=True)

            if response.status_code == 200:
                upload = cloudinary.uploader.upload(
                    ContentFile(response.content),
                    folder="menu_images",
                    public_id=item.name.replace(" ", "_"),
                    overwrite=True,
                    resource_type="image"
                )
                item.image = upload["secure_url"]
                item.save()
                print(f"✅ Uploaded image for {item.name} (query: {q})")
                uploaded = True
                break

        # 3️⃣ Last fallback: force a generic placeholder food image
        if not uploaded:
            url = "https://source.unsplash.com/600x400/?food"
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                upload = cloudinary.uploader.upload(
                    ContentFile(response.content),
                    folder="menu_images",
                    public_id=item.name.replace(" ", "_"),
                    overwrite=True,
                    resource_type="image"
                )
                item.image = upload["secure_url"]
                item.save()
                print(f"⚠️ Used generic food image for {item.name}")
            else:
                print(f"❌ Failed completely for {item.name}")
