from django.core.management.base import BaseCommand
from ...models import Country
from ...constants import (GROUP_A, GROUP_B, GROUP_C, GROUP_D, GROUP_E, GROUP_F,
                          GROUP_G, GROUP_H)


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Populating the countries...')

        # Group A
        Country.objects.get_or_create(name="Russia", group=GROUP_A, flag_image='uploads/country/rus.png')
        Country.objects.get_or_create(name="Saudi Arabia", group=GROUP_A, flag_image='uploads/country/ksa.png')
        Country.objects.get_or_create(name="Egypt", group=GROUP_A, flag_image='uploads/country/egy.png')
        Country.objects.get_or_create(name="Uruguay", group=GROUP_A, flag_image='uploads/country/uru.png')

        # Group B

        Country.objects.get_or_create(name="Portugal", group=GROUP_B, flag_image='uploads/country/por.png')
        Country.objects.get_or_create(name="Spain", group=GROUP_B, flag_image='uploads/country/esp.png')
        Country.objects.get_or_create(name="Morocco", group=GROUP_B, flag_image='uploads/country/mar.png')
        Country.objects.get_or_create(name="IR Iran", group=GROUP_B, flag_image='uploads/country/irn.png')

        # Group C
        Country.objects.get_or_create(name="France", group=GROUP_C, flag_image='uploads/country/fra.png')
        Country.objects.get_or_create(name="Australia", group=GROUP_C, flag_image='uploads/country/aus.png')
        Country.objects.get_or_create(name="Peru", group=GROUP_C, flag_image='uploads/country/per.png')
        Country.objects.get_or_create(name="Denmark", group=GROUP_C, flag_image='uploads/country/den.png')

        # Group D

        Country.objects.get_or_create(name="Argentina", group=GROUP_D, flag_image='uploads/country/arg.png')
        Country.objects.get_or_create(name="Iceland", group=GROUP_D, flag_image='uploads/country/isl.png')
        Country.objects.get_or_create(name="Croatia", group=GROUP_D, flag_image='uploads/country/cro.png')
        Country.objects.get_or_create(name="Nigeria", group=GROUP_D, flag_image='uploads/country/nga.png')

        # Group E
        Country.objects.get_or_create(name="Brazil", group=GROUP_E, flag_image='uploads/country/bra.png')
        Country.objects.get_or_create(name="Switzerland", group=GROUP_E, flag_image='uploads/country/sui.png')
        Country.objects.get_or_create(name="Costa Rica", group=GROUP_E, flag_image='uploads/country/crc.png')
        Country.objects.get_or_create(name="Serbia", group=GROUP_E, flag_image='uploads/country/srb.png')

        # Group F

        Country.objects.get_or_create(name="Germany", group=GROUP_F, flag_image='uploads/country/ger.png')
        Country.objects.get_or_create(name="Mexico", group=GROUP_F, flag_image='uploads/country/mex.png')
        Country.objects.get_or_create(name="Sweden", group=GROUP_F, flag_image='uploads/country/swe.png')
        Country.objects.get_or_create(name="Korea Republic", group=GROUP_F, flag_image='uploads/country/kor.png')

        # Group G
        Country.objects.get_or_create(name="Belgium", group=GROUP_G, flag_image='uploads/country/bel.png')
        Country.objects.get_or_create(name="Panama", group=GROUP_G, flag_image='uploads/country/pan.png')
        Country.objects.get_or_create(name="Tunisia", group=GROUP_G, flag_image='uploads/country/tun.png')
        Country.objects.get_or_create(name="England", group=GROUP_G, flag_image='uploads/country/eng.png')

        # Group H

        Country.objects.get_or_create(name="Poland", group=GROUP_H, flag_image='uploads/country/pol.png')
        Country.objects.get_or_create(name="Senegal", group=GROUP_H, flag_image='uploads/country/sen.png')
        Country.objects.get_or_create(name="Colombia", group=GROUP_H, flag_image='uploads/country/col.png')
        Country.objects.get_or_create(name="Japan", group=GROUP_H, flag_image='uploads/country/jpn.png')

        self.stdout.write(self.style.SUCCESS('Successfully populated the countries...'))
