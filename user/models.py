from django.db import models
from django.contrib.auth.models import User


# Basic information
class Area(models.Model):
    """
    Where the dormitory is locate
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=10)
    faculty = models.ForeignKey(
        'Faculty',
        related_name='schools_in'
    )

    def __str__(self):
        return self.name


class Faculty(models.Model):
    """
    Faculty of Engineering, Faculty of Information etc.
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Dormitory(models.Model):
    area = models.ForeignKey(
        Area,
        related_name='dormitories'
    )
    serial_number = models.CharField(max_length=10)

    def __str__(self):
        return self.area.name + self.serial_number


# organization information
class BaseOrganization(models.Model):
    """
    Abstract, including student union and departments in student union
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class StudentUnion(BaseOrganization):
    school = models.ForeignKey(
        School,
        related_name='student_union_in',
        on_delete=models.SET_NULL,
        null=True
    )


class Department(BaseOrganization):
    student_union_belongs_to = models.ForeignKey(
        StudentUnion,
        related_name='departments',
        on_delete=models.CASCADE
    )


class JobTitle(models.Model):
    department = models.ForeignKey(
        Department,
        related_name='job_titles'
    )
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.department.student_union_belongs_to.name + self.department.name + self.name


# User information
class Student(models.Model):
    user = models.OneToOneField(User)
    student_number = models.CharField(max_length=15)
    school = models.ForeignKey(
        School,
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    dormitory = models.ForeignKey(
        Dormitory,
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    # setting_information
    # personal_information

    def __str__(self):
        return self.user.first_name + self.user.last_name + '(' + self.user.username + ')'


class Staff(models.Model):
    student = models.OneToOneField(Student)
    job_title = models.ForeignKey(
        JobTitle,
        related_name='staffs'
    )

    def __str__(self):
        return self.student.user.first_name + self.student.user.last_name + '(' + self.job_title.__str__() + ')'


