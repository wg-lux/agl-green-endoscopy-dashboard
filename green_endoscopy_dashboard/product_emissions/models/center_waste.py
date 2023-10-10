from django.db import models
    
class CenterWaste(models.Model):
    center = models.ForeignKey("agl_base_db.Center", on_delete=models.CASCADE)
    year = models.IntegerField()
    waste = models.ForeignKey("Waste", on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.ForeignKey("agl_base_db.Unit", on_delete=models.SET_NULL, null=True)
    emission_factor = models.ForeignKey("EmissionFactor", on_delete=models.SET_NULL, null=True)

    