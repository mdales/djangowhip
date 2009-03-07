from django.db import models

class Division(models.Model):
    division_id = models.IntegerField(primary_key=True)
    valid = models.IntegerField()
    division_date = models.DateField()
    division_number = models.IntegerField()
    division_name = models.TextField()
    source_url = models.TextField()
    motion = models.TextField()
    notes = models.TextField()
    debate_url = models.TextField()
    house = models.TextField()
    clock_time = models.TextField()
    
    def __unicode__(self):
        return self.division_name
        
        
class MOffice(models.Model):
    moffice_id = models.IntegerField(primary_key=True)
    dept = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    person = models.IntegerField()
    responsibility = models.CharField(max_length=100, default='')
    
    def __unicode__(self):
        return self.dept
    
    
class MP(models.Model):
    # here I'm afraid we need to deviate from the sql from public whip
    # they use first_name, last_name, constituency, and entered/left_house as key
    
    mp_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)    
    title = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    entered_house = models.DateField()
    left_house = models.DateField()
    left_reason = models.TextField()
    person = models.IntegerField()
    house = models.TextField()
    
    def __unicode__(self):
        return "%s %s %s" % (self.title, self.first_name, self.last_name)
    

class Vote(models.Model):
    division = models.ForeignKey(Division)
    mp = models.ForeignKey(MP)
    vote = models.TextField()
    
    def __unicode__(self):
        return "%s voted %s on %s" % (self.mp, self.division, self.vote)