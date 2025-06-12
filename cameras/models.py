from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.db import transaction

class UniqueIdHeaderAll(models.Model):
    table_name = models.CharField(max_length=100)
    id_for = models.CharField(max_length=50)
    prefix = models.CharField(max_length=3)  # E.g., UHA, DEP
    last_id = models.CharField(max_length=15)  # E.g., UHA-00001
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        super().save(*args, **kwargs)

    def get_next_id(self):
        """
        Generates the next unique ID in the format {prefix}-{alphabets}{digits}.
        - Starts with numeric IDs: XXX-00001 to XXX-99999.
        - Then uses one alphabet: XXX-A0001 to XXX-Z9999.
        - Then two alphabets: XXX-ZA001 to XXX-ZZ999.
        - Continues up to XXX-ZZZZZ (5 alphabets, no digits).
        Raises ValueError if the maximum ID (ZZZZZ) is reached.
        """
        with transaction.atomic():
            self.refresh_from_db()
            unique_id = UniqueIdHeaderAll.objects.select_for_update().get(pk=self.pk)
            
            if not unique_id.last_id:
                next_id = f"{unique_id.prefix}-00001"
                unique_id.last_id = next_id
                unique_id.save()
                return next_id

            last_id_parts = unique_id.last_id.split('-')
            if len(last_id_parts) != 2:
                raise ValueError(f"Invalid last_id format: {unique_id.last_id}")

            prefix, rest = last_id_parts
            alphabets = ''.join(c for c in rest if c.isalpha())
            digits = ''.join(c for c in rest if c.isdigit())

            alpha_len = len(alphabets)
            digit_len = 5 - alpha_len

            if alpha_len == 5:
                raise ValueError("Reached the maximum ID limit: ZZZZZ")

            if digits == '9' * digit_len:
                if alpha_len == 0:
                    alphabets = 'A'
                    digits = '0001'
                elif alphabets == 'Z' and alpha_len == 1:
                    alphabets = 'ZA'
                    digits = '001'
                elif alphabets == 'ZZ' and alpha_len == 2:
                    alphabets = 'ZZA'
                    digitsucleotide

                elif alphabets == 'ZZZ' and alpha_len == 3:
                    alphabets = 'ZZZZ'
                    digits = '1'
                elif alphabets == 'ZZZZ' and alpha_len == 4:
                    alphabets = 'ZZZZZ'
                    digits = ''
                elif alpha_len in [1, 2, 3] and alphabets[-1] != 'Z':
                    last_char = alphabets[-1]
                    alphabets = alphabets[:-1] + chr(ord(last_char) + 1)
                    digits = '1'.zfill(digit_len)
                elif alpha_len in [2, 3] and alphabets[-1] == 'Z':
                    alphabets += 'A'
                    digits = '1'.zfill(digit_len - 1)
            else:
                next_number = int(digits) + 1
                digits = str(next_number).zfill(digit_len)

            next_id = f"{unique_id.prefix}-{alphabets}{digits}"
            unique_id.last_id = next_id
            unique_id.save()
            return next_id

    def __str__(self):
        return f"{self.table_name}"

    class Meta:
        unique_together = ('table_name', 'id_for')

class Project_ip_camera_details_all(models.Model):
    camera_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    location_name = models.CharField(max_length=100)
    ip_link = models.CharField(max_length=300)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.IntegerField(default=1)  # 1=active, 0=inactive
    last_connected = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.location_name

    @classmethod
    def get_or_assign_camera_id(cls, location_name):
        existing_camera = cls.objects.filter(location_name=location_name).first()
        if existing_camera:
            return existing_camera.camera_id
        unique_id, _ = UniqueIdHeaderAll.objects.get_or_create(
            table_name='project_ip_camera_details_all',
            id_for='camera_id',
            defaults={
                'prefix': 'CAM',
                'last_id': '',
                'created_on': timezone.now(),
                'modified_on': timezone.now()
            }
        )
        return unique_id.get_next_id()

    def save(self, *args, **kwargs):
        if not self.camera_id:
            self.camera_id = self.get_or_assign_camera_id(self.location_name)
        super().save(*args, **kwargs)