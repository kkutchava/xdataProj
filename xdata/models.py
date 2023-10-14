# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clients(models.Model):
    username = models.CharField(unique=True, max_length=255)
    siteid = models.IntegerField()
    filterwordsid = models.IntegerField()
    tts_enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clients'


class Filterwords(models.Model):
    clientid = models.IntegerField(blank=True, null=True)
    word = models.CharField(max_length=255, blank=True, null=True)
    wordalias = models.CharField(db_column='wordAlias', max_length=1022, blank=True, null=True)  # Field name made lowercase.
    subwordalias = models.CharField(max_length=255, blank=True, null=True)
    stopword = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filterwords'
    
    def __str__(self):
        return self.word


class Notifications(models.Model):
    clientid = models.IntegerField()
    sms = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Sites(models.Model):
    id = models.IntegerField(primary_key=True)
    sitename = models.CharField(unique=True, max_length=128)
    internal_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sites'
    
    def __str__(self):
        return self.sitename


class Articles(models.Model):
    site = models.ForeignKey('Sites', models.CASCADE) #cascade since if site is deleted article will be deleted too
    clientid = models.ForeignKey('Clients', models.DO_NOTHING, db_column='clientid') 
    insert_date = models.DateTimeField()
    article_date = models.DateTimeField()
    autor = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=1022)
    article_name = models.TextField()
    article_text = models.TextField()
    visitors_count = models.IntegerField()
    is_top_artikle = models.IntegerField()
    screenshot_url = models.CharField(max_length=90, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    found_word = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'articles'
        unique_together = (('id', 'site'), ('url', 'clientid'),)