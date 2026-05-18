from django.db import models
from django.utils import timezone
from datetime import date, timedelta


class Responsavel(models.Model):
    VINCULO_CHOICES = [
        ('mae', 'Mãe'),
        ('pai', 'Pai'),
        ('avo', 'Avó / Avô'),
        ('tio', 'Tio / Tia'),
        ('responsavel_legal', 'Responsável legal'),
        ('outro', 'Vizinho / Outro'),
    ]

    nome = models.CharField('Nome completo', max_length=200)
    telefone = models.CharField('Telefone / WhatsApp', max_length=20)
    vinculo = models.CharField('Vínculo com a criança', max_length=30, choices=VINCULO_CHOICES)
    bairro = models.CharField('Bairro / Comunidade', max_length=100, blank=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def aniversario_esta_semana(self):
        if not self.data_nascimento:
            return False
        hoje = date.today()
        for i in range(7):
            dia = hoje + timedelta(days=i)
            if dia.month == self.data_nascimento.month and dia.day == self.data_nascimento.day:
                return True
        return False


class Crianca(models.Model):
    nome = models.CharField('Nome completo', max_length=200)
    data_nascimento = models.DateField('Data de nascimento')
    escola = models.CharField('Escola onde estuda', max_length=200, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Criança / Adolescente'
        verbose_name_plural = 'Crianças / Adolescentes'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def aniversario_esta_semana(self):
        hoje = date.today()
        for i in range(7):
            dia = hoje + timedelta(days=i)
            if dia.month == self.data_nascimento.month and dia.day == self.data_nascimento.day:
                return True
        return False


class Atendimento(models.Model):
    TIPO_CHOICES = [
        ('violencia_fisica', 'Violência física'),
        ('violencia_psicologica', 'Violência psicológica'),
        ('negligencia', 'Negligência'),
        ('abandono', 'Abandono'),
        ('evasao_escolar', 'Evasão escolar'),
        ('abuso_sexual', 'Abuso sexual'),
        ('trabalho_infantil', 'Trabalho infantil'),
        ('outro', 'Outro'),
    ]

    ENCAMINHAMENTO_CHOICES = [
        ('', 'Nenhum por enquanto'),
        ('cras', 'CRAS'),
        ('creas', 'CREAS'),
        ('ubs', 'UBS / Posto de saúde'),
        ('delegacia', 'Delegacia'),
        ('escola', 'Escola'),
        ('mp', 'Ministério Público'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em andamento'),
        ('encerrado', 'Encerrado'),
    ]

    numero_protocolo = models.CharField('Nº do atendimento', max_length=20, unique=True, editable=False)
    crianca = models.ForeignKey(Crianca, on_delete=models.PROTECT, related_name='atendimentos', verbose_name='Criança / Adolescente')
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT, related_name='atendimentos', verbose_name='Responsável')
    tipo_demanda = models.CharField('Tipo de demanda', max_length=30, choices=TIPO_CHOICES)
    descricao = models.TextField('Descrição do atendimento')
    encaminhamento = models.CharField('Encaminhamento realizado', max_length=30, choices=ENCAMINHAMENTO_CHOICES, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberto')
    data_hora = models.DateTimeField('Data e hora', default=timezone.now)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'
        ordering = ['-data_hora']

    def __str__(self):
        return f'{self.numero_protocolo} — {self.crianca.nome}'

    def save(self, *args, **kwargs):
        if not self.numero_protocolo:
            ano = timezone.now().year
            ultimo = Atendimento.objects.filter(
                numero_protocolo__startswith=f'CT-{ano}-'
            ).count()
            self.numero_protocolo = f'CT-{ano}-{str(ultimo + 1).zfill(5)}'
        super().save(*args, **kwargs)
