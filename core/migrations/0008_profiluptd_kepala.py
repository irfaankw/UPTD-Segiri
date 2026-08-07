from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0004_anggota_sambutan_singkat'),
        ('core', '0007_remove_herobannerutama_deskripsi_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiluptd',
            name='nama_kepala',
        ),
        migrations.RemoveField(
            model_name='profiluptd',
            name='jabatan_kepala',
        ),
        migrations.AddField(
            model_name='profiluptd',
            name='kepala',
            field=models.ForeignKey(
                blank=True,
                help_text='Pilih dari data Anggota berkategori Pimpinan.',
                limit_choices_to={'kategori': 'pimpinan'},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='profil_uptd',
                to='membership.anggota',
            ),
        ),
    ]