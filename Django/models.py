from django.db import models
from xadmin.models import UserSettings  # 映入 xadmin 用户表
from DjangoUeditor.models import UEditorField

"""
	tb_user
	tb_role
	tb_permiss


	tb_banner 系统前台首页轮播图
    tb_menu   系统菜单导航
    tb_label  系统标签


	

    tb_course
    tb_section
    tb_video
    tb_article
    tb_resource
    tb_comments
"""


# Create your models here.

class Course(models.Model):
    """ 课程模型表 """

    class Meta:
        db_table = 'tb_course'  # 模型映射到数据库名称
        verbose_name = "课程-基本信息"
        verbose_name_plural = verbose_name

    # 课程状态枚举
    CourseStatus = (
        ('close', '未开放'),
        ('open', '公开课'),
        ('private', '内部课'),
    )

    course_name = models.CharField('课程名称', max_length=48, default='无')
    course_desc = models.CharField('课程描述', max_length=512)
    course_status = models.CharField('课程状态', choices=CourseStatus, max_length=12)
    course_created_time = models.DateTimeField('创建时间', auto_now_add=True)
    course_updated_time = models.DateTimeField('最后一次更新时间', auto_now_add=True)

    def __str__(self): return self.course_name


class Lesson(models.Model):
    """ 课程章节模型表 """

    class Meta:
        db_table = 'tb_course_lesson'  # 模型映射到数据库名称
        verbose_name = "课程-章节"
        verbose_name_plural = verbose_name

    lesson_name = models.CharField('章节名称', max_length=48, default='章节名')
    lesson_son = models.BooleanField('是否是末尾章节', default=True)
    lesson_created_time = models.DateTimeField('创建时间', auto_now_add=True)
    lesson_updated_time = models.DateTimeField('最后一次更新时间', auto_now_add=True)

    # 设置外键: 章节属于哪个课程
    lesson_fk_course = models.ForeignKey(verbose_name='课程', to=Course, on_delete=models.CASCADE)

    # 设置外键: 章节是属于哪个子章节:
    lesson_fk_lesson = models.ForeignKey(verbose_name='父章节', to='self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '《{}》- lesson: {}'.format(self.lesson_fk_course, self.lesson_name)


class Video(models.Model):
    """ 课程视频模型表 """

    class Meta:
        db_table = 'tb_course_video'  # 模型映射到数据库名称
        verbose_name = "课程-视频"
        verbose_name_plural = verbose_name

    video_name = models.CharField('视频名称', max_length=48, default='无')
    video_desc = models.CharField('视频简介', max_length=256, default='无')
    video_url = models.CharField('视频资源路径', max_length=256, default='#')
    video_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 视频属于哪个章节
    video_fk_lesson = models.ForeignKey(verbose_name='章节', to=Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - video: {}'.format(self.video_fk_lesson, self.video_name)


class Article(models.Model):
    """  """
    class Meta:
        db_table = 'tb_course_article'  # 模型映射到数据库名称
        verbose_name = "课程-文章"
        verbose_name_plural = verbose_name

    article_name = models.CharField('文章名称', max_length=48, default='无')
    article_desc = UEditorField(verbose_name='文章内容', default='', width='100%')
    article_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 视频属于哪个章节
    article_fk_lesson = models.ForeignKey(verbose_name='章节', to=Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - article: {}'.format(self.article_fk_lesson, self.article_name)



class Resource(models.Model):
    """ 课程资源模型表 """

    class Meta:
        db_table = 'tb_course_resource'  # 模型映射到数据库名称
        verbose_name = "课程-资料"
        verbose_name_plural = verbose_name

    res_name = models.CharField('资源名称', max_length=48, default='res')
    res_url = models.CharField('资源路径', max_length=256, default='#')
    res_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 课程资源属于哪个章节
    res_fk_lesson = models.ForeignKey(verbose_name='章节', to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.res_name


class Comments(models.Model):
    """ 课程评论模型表 """

    class Meta:
        db_table = 'tb_course_comments'  # 模型映射到数据库名称
        verbose_name = "课程-评论"
        verbose_name_plural = verbose_name

    comments_name = models.CharField('评论名称', max_length=48, default='menu')
    comments_msg = models.CharField('评论内容', max_length=1000, default='#')
    comments_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 评论属于哪个课程
    comments_fk_course = models.ForeignKey(verbose_name='课程', to=Course, on_delete=models.CASCADE)

    # 设置外键: 评论属于哪个用户
    comments_fk_user = models.ForeignKey(verbose_name='用户', to=UserSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.comments_name









class Banner(models.Model):
    """ 系统轮播图模型表 """

    class Meta:
        db_table = 'tb_banner'  # 模型映射到数据库名称
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    banner_title = models.CharField('轮播图标题', max_length=48, default='无')
    banner_index = models.IntegerField('轮播图顺序', default=1)
    banner_url = models.CharField('轮播图图片地址', max_length=128, default='#')
    banner_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self): return self.banner_title


class Menu(models.Model):
    """ 系统菜单导航模型表 """

    class Meta:
        db_table = 'tb_menu'  # 模型映射到数据库名称
        verbose_name = "系统菜单(导航栏)"
        verbose_name_plural = verbose_name

    menu_title = models.CharField('菜单标题', max_length=48, default='无')
    menu_level = models.IntegerField('菜单层级', default=0)
    menu_url = models.CharField('菜单链接地址', max_length=128, default='#')
    menu_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置菜单导航栏数据库表自关联
    menu_parent = models.ForeignKey(verbose_name='父级菜单', to='self', null=True, blank=True)

    def __str__(self): return self.menu_title

































