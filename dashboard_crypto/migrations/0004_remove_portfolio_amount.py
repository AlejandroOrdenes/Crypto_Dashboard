# Generated by Django 4.1.7 on 2023-03-02 16:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard_crypto", "0003_portfolio_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="portfolio",
            name="amount",
        ),
    ]