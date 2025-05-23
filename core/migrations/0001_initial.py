# Generated by Django 4.2.20 on 2025-04-22 02:27

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[("admin", "Administrador"), ("usuario", "Usuário")],
                        default="usuario",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "Usuário",
                "verbose_name_plural": "Usuários",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Agendamento",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("diario", "Diário"),
                            ("semanal", "Semanal"),
                            ("mensal", "Mensal"),
                        ],
                        max_length=20,
                    ),
                ),
                ("dias", models.CharField(blank=True, max_length=255)),
                ("horario", models.TimeField()),
                ("ativo", models.BooleanField(default=True)),
                (
                    "data_criacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("ultima_execucao", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Agendamento",
                "verbose_name_plural": "Agendamentos",
            },
        ),
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255, unique=True)),
                (
                    "data_criacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "Cliente",
                "verbose_name_plural": "Clientes",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="ClienteGrupo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "data_associacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.cliente"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dominio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255, unique=True)),
                ("seletor_css", models.CharField(max_length=1000)),
                (
                    "data_criacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "Domínio",
                "verbose_name_plural": "Domínios",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Grupo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_grupo", models.CharField(max_length=255, unique=True)),
                ("nome", models.CharField(max_length=255)),
                ("descricao", models.TextField(blank=True)),
                (
                    "data_criacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "clientes",
                    models.ManyToManyField(
                        related_name="grupos",
                        through="core.ClienteGrupo",
                        to="core.cliente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Grupo",
                "verbose_name_plural": "Grupos",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Plataforma",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255, unique=True)),
                ("seletor_css", models.CharField(max_length=1000)),
                (
                    "data_criacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "Plataforma",
                "verbose_name_plural": "Plataformas",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="UsuarioGrupo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "data_associacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "grupo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.grupo"
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("usuario", "grupo")},
            },
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("concorrente", models.CharField(max_length=255)),
                ("url", models.URLField(max_length=1000)),
                (
                    "data_criacao",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("ultima_verificacao", models.DateTimeField(blank=True, null=True)),
                ("posicao_fila", models.IntegerField(default=0)),
                ("verificacao_manual", models.BooleanField(default=False)),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="produtos",
                        to="core.cliente",
                    ),
                ),
                (
                    "grupo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="produtos",
                        to="core.grupo",
                    ),
                ),
                (
                    "plataforma",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="produtos",
                        to="core.plataforma",
                    ),
                ),
            ],
            options={
                "verbose_name": "Produto",
                "verbose_name_plural": "Produtos",
                "ordering": ["-data_criacao"],
                "unique_together": {("cliente", "nome", "url")},
            },
        ),
        migrations.AddField(
            model_name="grupo",
            name="usuarios",
            field=models.ManyToManyField(
                related_name="grupos",
                through="core.UsuarioGrupo",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="clientegrupo",
            name="grupo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.grupo"
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="cliente_atual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="usuarios_ativos",
                to="core.cliente",
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.CreateModel(
            name="HistoricoPreco",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                ("data", models.DateField(default=django.utils.timezone.now)),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="historico_precos",
                        to="core.produto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Histórico de Preço",
                "verbose_name_plural": "Histórico de Preços",
                "ordering": ["-data"],
                "indexes": [
                    models.Index(
                        fields=["produto", "data"],
                        name="core_histor_produto_ade677_idx",
                    )
                ],
            },
        ),
        migrations.AlterUniqueTogether(
            name="clientegrupo",
            unique_together={("cliente", "grupo")},
        ),
    ]
