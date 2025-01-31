from django.db import models

class Classroom(models.Model):
    classID = models.AutoField(primary_key=True)
    className = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.className

class FacultyData(models.Model):
    facultyID = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=15)
    facultyName = models.CharField(max_length=255)
    facultyDesignation = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True)
    assigned_classes = models.ManyToManyField(Classroom, related_name="faculty_classes")

    def __str__(self):
        return self.facultyName

