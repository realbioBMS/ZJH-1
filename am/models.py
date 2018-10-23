from django.db import models
from django.contrib.auth.models import User
from pm.models import AnaSubmit


class AnaExecute(models.Model):
    """执行生信分析步骤"""
    ana_submit = models.OneToOneField(
        AnaSubmit, verbose_name="子项目编号（分析）"
    )
    analyst = models.ForeignKey(
        User, verbose_name="生信分析员"
    )
    end_date = models.DateField(
        verbose_name="实际结束日期", blank=True, null=True
    )
    submit_date = models.DateField(
        verbose_name="分析提交日期", auto_now_add=True
    )
    confirmation_sheet = models.URLField(
        verbose_name="分析确认单", max_length=512, blank=True, null=True
    )
    ana_result_path = models.CharField(
        verbose_name="分析结果路径", max_length=512, blank=True, null=True
    )
    baidu_link = models.CharField(
        verbose_name="分析结果链接", max_length=512, blank=True, null=True
    )
    notes = models.TextField(
        verbose_name="备注", null=True, blank=True
    )
    is_submit = models.BooleanField(
        verbose_name="是否提交", default=False,
    )
    
    class Meta:
        verbose_name = '4分析任务执行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.ana_submit.ana_slug
