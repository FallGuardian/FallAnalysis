# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Asus(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'ASUS'

class Htc(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'HTC'

class Sma(models.Model):
    label = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    sma = models.FloatField(null=True, db_column='SMA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SMA'

class AdjustId(models.Model):
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'adjust_id'

class Age0(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age0'

class Age1(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age1'

class Age2(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age2'

class Age201(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age201'

class Age3(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age3'

class Age4(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age4'

class Age5(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age5'

class Age6(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age6'

class Age7(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age7'

class Age8(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age8'

class Age9(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'age9'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=240)
    class Meta:
        db_table = u'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = u'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    content_type = models.ForeignKey(DjangoContentType)
    codename = models.CharField(unique=True, max_length=300)
    class Meta:
        db_table = u'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=384)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=90)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = u'auth_user_user_permissions'

class Bio(models.Model):
    serial = models.CharField(max_length=54, primary_key=True)
    svm = models.FloatField(null=True, db_column='SVM', blank=True) # Field name made lowercase.
    av = models.FloatField(null=True, db_column='AV', blank=True) # Field name made lowercase.
    ta = models.FloatField(null=True, db_column='TA', blank=True) # Field name made lowercase.
    dots = models.IntegerField(null=True, blank=True)
    svmact = models.IntegerField(null=True, db_column='SVMact', blank=True) # Field name made lowercase.
    avact = models.IntegerField(null=True, db_column='AVact', blank=True) # Field name made lowercase.
    sma = models.FloatField(null=True, db_column='SMA', blank=True) # Field name made lowercase.
    aact = models.IntegerField(null=True, db_column='Aact', blank=True) # Field name made lowercase.
    th1a = models.FloatField(null=True, db_column='Th1a', blank=True) # Field name made lowercase.
    th1b = models.FloatField(null=True, db_column='Th1b', blank=True) # Field name made lowercase.
    orientation = models.FloatField(null=True, blank=True)
    sample = models.IntegerField(null=True, blank=True)
    samplesvm = models.FloatField(null=True, db_column='sampleSVM', blank=True) # Field name made lowercase.
    sampleav = models.FloatField(null=True, db_column='sampleAV', blank=True) # Field name made lowercase.
    csvm = models.FloatField(null=True, db_column='CSVM', blank=True) # Field name made lowercase.
    cact = models.IntegerField(null=True, db_column='Cact', blank=True) # Field name made lowercase.
    bact = models.IntegerField(null=True, db_column='Bact', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'bio'

class Calculated(models.Model):
    label = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    svm = models.FloatField(null=True, db_column='SVM', blank=True) # Field name made lowercase.
    ta = models.FloatField(null=True, db_column='TA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'calculated'

class Checkpoints(models.Model):
    id = models.IntegerField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'checkpoints'

class CheckpointsLater(models.Model):
    id = models.IntegerField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'checkpoints_later'

class Chest(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'chest'

class Data(models.Model):
    sn = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    ta = models.FloatField(null=True, db_column='TA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'daTA'

class Data(models.Model):
    label = models.FloatField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    accelerate_x = models.FloatField(null=True, blank=True)
    accelerate_y = models.FloatField(null=True, blank=True)
    accelerate_z = models.FloatField(null=True, blank=True)
    gyro_x = models.FloatField(null=True, blank=True)
    gyro_y = models.FloatField(null=True, blank=True)
    gyro_z = models.FloatField(null=True, blank=True)
    time_acc = models.FloatField(null=True, blank=True)
    time_gyro = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'data'

class Datarevisit(models.Model):
    label = models.IntegerField(null=True, blank=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    svm = models.FloatField(null=True, db_column='SVM', blank=True) # Field name made lowercase.
    ta = models.FloatField(null=True, db_column='TA', blank=True) # Field name made lowercase.
    vv = models.FloatField(null=True, db_column='Vv', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'dataRevisit'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=600)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, null=True, blank=True)
    user = models.ForeignKey(AuthUser)
    class Meta:
        db_table = u'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    app_label = models.CharField(unique=True, max_length=300)
    model = models.CharField(unique=True, max_length=300)
    class Meta:
        db_table = u'django_content_type'

class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    applied = models.DateTimeField()
    class Meta:
        db_table = u'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class FallId(models.Model):
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'fall_id'

class Female(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'female'

class FormatedData(models.Model):
    base_id = models.IntegerField()
    id = models.IntegerField()
    ta = models.FloatField(db_column='TA') # Field name made lowercase.
    sma = models.FloatField(db_column='SMA') # Field name made lowercase.
    svm = models.FloatField(db_column='SVM') # Field name made lowercase.
    label = models.IntegerField()
    class Meta:
        db_table = u'formated_data'

class Height(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height'

class Height0(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height0'

class Height1(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height1'

class Height10(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height10'

class Height2(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height2'

class Height3(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height3'

class Height4(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height4'

class Height5(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height5'

class Height6(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height6'

class Height7(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height7'

class Height8(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height8'

class Height9(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'height9'

class IdBase(models.Model):
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'id_base'

class Kilogram(models.Model):
    id = models.IntegerField(primary_key=True)
    intl = models.CharField(max_length=24, blank=True)
    class Meta:
        db_table = u'kilogram'

class LabPrimitive(models.Model):
    id = models.IntegerField()
    acc_x = models.FloatField(null=True, blank=True)
    acc_y = models.FloatField(null=True, blank=True)
    acc_z = models.FloatField(null=True, blank=True)
    gyro_x = models.FloatField(null=True, blank=True)
    gyro_y = models.FloatField(null=True, blank=True)
    gyro_z = models.FloatField(null=True, blank=True)
    time_acc = models.IntegerField(null=True, blank=True)
    time_gyro = models.IntegerField(null=True, blank=True)
    svm = models.FloatField(null=True, db_column='SVM', blank=True) # Field name made lowercase.
    av = models.FloatField(null=True, db_column='AV', blank=True) # Field name made lowercase.
    gravity_x = models.FloatField(null=True, blank=True)
    gravity_y = models.FloatField(null=True, blank=True)
    gravity_z = models.FloatField(null=True, blank=True)
    ta = models.FloatField(db_column='TA') # Field name made lowercase.
    sma = models.FloatField(db_column='SMA') # Field name made lowercase.
    time_stamp = models.IntegerField()
    class Meta:
        db_table = u'lab_primitive'

class Male(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'male'

class Orientation(models.Model):
    label = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    result = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'orientation'

class Outcast(models.Model):
    debug = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'outcast'

class Purse(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'purse'

class Samsung(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'samsung'

class StandId(models.Model):
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'stand_id'

class Tall(models.Model):
    id = models.IntegerField(primary_key=True)
    intl = models.CharField(max_length=24, blank=True)
    class Meta:
        db_table = u'tall'

class Thigh(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'thigh'

class Tmp(models.Model):
    id = models.IntegerField(primary_key=True)
    ta = models.FloatField(db_column='TA') # Field name made lowercase.
    sma = models.FloatField(db_column='SMA') # Field name made lowercase.
    class Meta:
        db_table = u'tmp'

class Tryout(models.Model):
    label = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    time = models.FloatField(null=True, blank=True)
    accelerator_x = models.FloatField(null=True, blank=True)
    accelerator_y = models.FloatField(null=True, blank=True)
    accelerator_z = models.FloatField(null=True, blank=True)
    gyro = models.FloatField(null=True, blank=True)
    gyro_y = models.FloatField(null=True, blank=True)
    gyro_z = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'tryout'

class Velocity(models.Model):
    label = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    velocity = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'velocity'

class Waist(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'waist'

class Weight(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight'

class Weight3(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight3'

class Weight4(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight4'

class Weight5(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight5'

class Weight6(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight6'

class Weight7(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight7'

class Weight8(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight8'

class Weight9(models.Model):
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'weight9'

class Year(models.Model):
    id = models.IntegerField(primary_key=True)
    intl = models.CharField(max_length=21, blank=True)
    class Meta:
        db_table = u'year'

