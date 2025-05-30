from django.core.management.base import BaseCommand

from analysis.models import JewelryInventory, JewelrySales


class Command(BaseCommand):
    help = "Seeds sample jewelry data"

    def handle(self, *args, **kwargs):
        sales = [
            {"code": "J001", "tags": "yellow-gold,bracelet,peacock-motif"},
            {"code": "J002", "tags": "platinum,necklace,floral-pattern"},
            {"code": "J003", "tags": "yellow-gold,ring,green-beads"},
            {"code": "J004", "tags": "yellow-gold,bracelet,floral-pattern"},
            {"code": "J005", "tags": "silver,earrings,peacock-motif"},
            {"code": "J006", "tags": "yellow-gold,necklace,green-beads"},
            {"code": "J007", "tags": "platinum,bracelet,peacock-motif"},
            {"code": "J008", "tags": "yellow-gold,ring,floral-pattern"},
            {"code": "J009", "tags": "silver,necklace,green-beads"},
            {"code": "J010", "tags": "yellow-gold,bracelet,peacock-motif"},
            {"code": "J011", "tags": "platinum,earrings,floral-pattern"},
            {"code": "J012", "tags": "yellow-gold,ring,green-beads"},
            {"code": "J013", "tags": "silver,bracelet,peacock-motif"},
            {"code": "J014", "tags": "yellow-gold,necklace,floral-pattern"},
            {"code": "J015", "tags": "platinum,ring,green-beads"},
            {"code": "J016", "tags": "yellow-gold,bracelet,peacock-motif"},
            {"code": "J017", "tags": "silver,earrings,floral-pattern"},
            {"code": "J018", "tags": "yellow-gold,necklace,green-beads"},
            {"code": "J019", "tags": "platinum,bracelet,peacock-motif"},
            {"code": "J020", "tags": "yellow-gold,ring,floral-pattern"},
        ]
        inventory = [
            {"code": "I001", "tags": "silver,earrings,star-motif"},
            {"code": "I002", "tags": "platinum,bracelet,geometric-pattern"},
            {"code": "I003", "tags": "rose-gold,necklace,heart-motif"},
            {"code": "I004", "tags": "silver,ring,moon-pattern"},
            {"code": "I005", "tags": "platinum,earrings,star-motif"},
        ]
        for item in sales:
            JewelrySales.objects.get_or_create(
                jewelry_code=item["code"], product_tags=item["tags"]
            )
        for item in inventory:
            JewelryInventory.objects.get_or_create(
                jewelry_code=item["code"], product_tags=item["tags"]
            )
        self.stdout.write(self.style.SUCCESS("Seeded 20 sales and 5 inventory records"))
