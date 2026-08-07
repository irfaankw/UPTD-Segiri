from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_profiluptd_kepala'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiluptd',
            name='kepala',
        ),
        migrations.AddField(
            model_name='profiluptd',
            name='nama_kepala',
            # default='' cuma dipakai SEKALI buat ngisi baris lama yang udah ada
            # (biar gak bentrok NOT NULL). preserve_default=False artinya default ini
            # TIDAK disimpan sebagai default permanen di model — cocok sama core/models.py
            # yang emang nama_kepala-nya gak punya default.
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profiluptd',
            name='jabatan_kepala',
            field=models.CharField(default='Kepala UPTD Pasar Segiri', max_length=150),
        ),
    ]