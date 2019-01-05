from django.db import models
from xadmin.models import UserSettings  # 映入 xadmin 用户表
from DjangoUeditor.models import UEditorField

    
"""
    人员 : 实际使用系统的用户，也就是需要进行权限检查的人
  * 组织 : 树形结构，但是人员可以属于一个或者多个组织
  * 资源 : 需要授权的东西都可以认为是资源，每个功能是资源，每个接口也是资源，每条数据也是资源。
  * 动作 : 对资源的操作， CRUD
    权限 : 组织 + 资源 + 动作 （什么人对什么资源可以做什么动作）

    人员 - 组织  多对多 
    
"""


    
class User(models.Model):
    """ 用户模型表 """

    class Meta:
        db_table = 'tb_user'  # 模型映射到数据库名称
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    Questions = (
        ('1', '我的生日是多少'),
        ('2', '父亲生日是多少'),
        ('3', '母亲生日是多少'),
        ('4', '其他验证问题'),
    )

    user_name = models.CharField('用户名称', max_length=48, default='无')
    user_pwd = models.CharField('用户密码', max_length=128, default='无')
    user_img = models.CharField('用户头像', max_length=128, default='#')
    user_email = models.CharField('用户邮箱', max_length=128, default='无')
    user_tel = models.CharField('用户座机', max_length=12, default='无')
    user_phone = models.CharField('用户手机', max_length=12, default='无')

    user_question = models.CharField('安全验证问题', max_length=64, default='无', choices=Questions)
    user_answer = models.CharField('安全验证答案', max_length=64, default='无')
    
    user_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user_modify_time = models.DateTimeField('最后修改时间', auto_now_add=True)
    
    # 用户与组织多对多关联:
    user_org = models.ManyToManyField(verbose_name="用户组织", to="Org", null=True, blank=True)
    
    def __str__(self): 
        return self.user_name
    
    
class Org(models.Model):
    """ 组织表 """
    class Meta:
        db_table = 'tb_org'  # 模型映射到数据库名称
        verbose_name = "组织"
        verbose_name_plural = verbose_name
        
    org_name = models.CharField("组织名称", max_length=36, default='无')
    org_level = models.IntegerField('组织层级', default=0)  # 可以理解成组织分类
    
    org_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置组织的父级组织
    org_parent = models.ForeignKey(verbose_name='父级组织', to='self', null=True, blank=True)

    def __str__(self):
        return self.org_name


class Res(models.Model):
    """ 抽象资源表 """
    class Meta:
        db_table = 'tb_res'  # 模型映射到数据库名称
        verbose_name = "资源表"
        verbose_name_plural = verbose_name
        
    res_name = models.CharField("资源名称", max_length=36, default='无')
    res_type = models.CharField('资源类型', default=0)
    res_code = models.CharField('资源唯一标示', default=0)
    
    # 资源也应该是一个树形结构
    res_parent = models.ForeignKey(verbose_name='父级资源', to='self', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.res_name
   

class Action(models.Model):
    """ 操作表，动作表 """
    class Meta:
        db_table = 'tb_action'  # 模型映射到数据库名称
        verbose_name = "操作"
        verbose_name_plural = verbose_name
        
    Options = (
        ('POST', '新增'),
        ('GET', '查询'),
        ('PUT', '修改'),
        ('DEL', '删除'),
    )

    action_name = models.CharField("操作名称", max_length=36, default='无', choices=Options)
    
    def __str__(self):
        return self.action_name


class Permission(models.Model):
    """ 权限表: 需要动态绑定 -->  什么人  什么资源  可以做什么  """
    class Meta:
        db_table = 'tb_permission'  # 模型映射到数据库名称
        verbose_name = "权限表"
        verbose_name_plural = verbose_name
        
    permission_name = models.CharField("权限名称", max_length=36, default='可以不填')
    permission_org = models.ForeignKey(verbose_name='什么组织', to=Org, null=True, blank=True)
    permission_res = models.ForeignKey(verbose_name='什么资源', to=Res, null=True, blank=True)
    permission_action = models.ForeignKey(verbose_name='什么操作', to=Action, null=True, blank=True)
    
    def __str__(self):
        return self.permission_name




        
""" ======================================================================================= """





class Menu(models.Model):
    """ 系统菜单资源表 
    每个功能、资源 当成一个菜单，菜单有url属性，用户通过点击菜单来访问对应功能、资源
    """

    class Meta:
        db_table = 'tb_menu'  # 模型映射到数据库名称
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    menu_code = models.IntegerField('菜单唯一标示', default=0)  # 用来去除主键带来的变更性
    menu_title = models.CharField('菜单标题', max_length=48, default='无')
    menu_level = models.IntegerField('菜单层级', default=0)
    menu_url = models.CharField('菜单链接地址', max_length=128, default='#')
    menu_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置菜单导航栏数据库表自关联
    menu_parent = models.ForeignKey(verbose_name='父级菜单', to='self', null=True, blank=True)
    
    # 设置菜单资源表与 Res 抽象资源表一对一映射
    menu_res = models.OneToOneField(to=Res, on_delete=models.CASCADE)

    def __str__(self): return self.menu_title




class Banner(models.Model):
    """ 系统轮播图模型表 
    也可以将其变成可授权资源（没必要，轮播图大家都可以看）
    """

    class Meta:
        db_table = 'tb_banner'  # 模型映射到数据库名称
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    banner_title = models.CharField('轮播图标题', max_length=48, default='无')
    banner_index = models.IntegerField('轮播图顺序', default=1)
    banner_url = models.CharField('轮播图图片地址', max_length=128, default='#')
    banner_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self): return self.banner_title






""" ======================================================================================= """






class Course(models.Model):
    """ 课程模型表 
    这个 课程感觉需要添加到 资源管理里去
    """

    class Meta:
        db_table = 'tb_course'  # 模型映射到数据库名称
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    # 课程状态枚举
    CourseStatus = (
        ('close', '未开放'),
        ('public', '公开课'),
        ('private', '内部课'),
    )

    course_name = models.CharField('课程名称', max_length=48, default='无')
    course_desc = models.CharField('课程描述', max_length=512)
    course_status = models.CharField('课程状态', choices=CourseStatus, max_length=12)
    course_created_time = models.DateTimeField('创建时间', auto_now_add=True)
    course_updated_time = models.DateTimeField('最后一次更新时间', auto_now_add=True)

    # 设置课程资源表与 Res 抽象资源表一对一映射
    course_res = models.OneToOneField(to=Res, on_delete=models.CASCADE)

    def __str__(self): 
        return self.course_name


class Lesson(models.Model):
    """ 课程章节模型表 
    可能重命名: section 会好一点
    """

    class Meta:
        db_table = 'tb_lesson'  # 模型映射到数据库名称
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
        return '《{}》- part: {}'.format(self.lesson_fk_course, self.lesson_name)


class Article(models.Model):
    """ 课程文章模型表 """
    class Meta:
        db_table = 'tb_article'  # 模型映射到数据库名称
        verbose_name = "文章教程"
        verbose_name_plural = verbose_name

    article_name = models.CharField('文章名称', max_length=48, default='无')
    article_desc = UEditorField(verbose_name='文章内容', default='', width='100%')
    article_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 视频属于哪个章节
    article_fk_lesson = models.ForeignKey(verbose_name='章节', to=Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - article: {}'.format(self.article_fk_lesson, self.article_name)


class Video(models.Model):
    """ 课程视频模型表 """
    class Meta:
        db_table = 'tb_video'  # 模型映射到数据库名称
        verbose_name = "视频教程"
        verbose_name_plural = verbose_name

    video_name = models.CharField('视频名称', max_length=48, default='无')
    video_desc = models.CharField('视频简介', max_length=256, default='无')
    video_url = models.CharField('视频资源路径', max_length=256, default='#')
    video_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 视频属于哪个章节
    video_fk_lesson = models.ForeignKey(verbose_name='章节', to=Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - video: {}'.format(self.video_fk_lesson, self.video_name)


class Resource(models.Model):
    """ 课程资源模型表 """
    class Meta:
        db_table = 'tb_resource'  # 模型映射到数据库名称
        verbose_name = "相关资料"
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
        db_table = 'tb_comments'  # 模型映射到数据库名称
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    comments_name = models.CharField('评论名称', max_length=48, default='menu')
    comments_msg = models.CharField('评论内容', max_length=1000, default='#')
    comments_created_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 设置外键: 评论属于哪个课程
    comments_fk_course = models.ForeignKey(verbose_name='课程', to=Course, on_delete=models.CASCADE, null=True, blank=True)

    # 设置外键: 评论属于哪个用户
    comments_fk_user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.comments_name






""" ======================================================================================= """





 
"""    系统考试数据库分析     """ 
# 题库, 试卷头表, 试卷详细表, 考试成绩表

class Questions(models.Model):
    """ 试题库模型表 """

    class Meta:
        db_table = 'tb_question'  # 模型映射到数据库名称
        verbose_name = "试题库"
        verbose_name_plural = verbose_name

    question_type = (
        (1, '单选题'),
        (2, '多选题'),
        (3, '判断题'),
    )

    question_name = models.CharField('试题名称', max_length=1024, default='无')
    question_type = models.IntegerField('试题类型', choices=question_type)
    question_answer = models.CharField('问题答案', max_length=1024, default='无')
    question_mark = models.IntegerField('试题是否选中', default=0)
    question_score = models.IntegerField('试题分数', default=4)
    question_option1 = models.CharField('预备选项1', max_length=1024, default='无')
    question_option2 = models.CharField('预备选项2', max_length=1024, default='无')
    question_option3 = models.CharField('预备选项3', max_length=1024, default='无')
    question_option4 = models.CharField('预备选项4', max_length=1024, default='无')
    question_option5 = models.CharField('预备选项5', max_length=1024, default='无')
    question_option6 = models.CharField('预备选项6', max_length=1024, default='无')

    question_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    question_modify_time = models.DateTimeField('最后一次更新时间', auto_now_add=True)

    # 设置一对多: 该试题属于哪个试卷
    question_exams = models.ManyToManyField(verbose_name="试卷", to="Exams", null=True, blank=True)

    # 设置外键: 试题属于哪个课程
    question_fk_course = models.ForeignKey(verbose_name='课程', to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_name 



class Exams(models.Model):
    """ 试卷模型表 """
    class Meta:
        db_table = 'tb_question'  # 模型映射到数据库名称
        verbose_name = "试题库"
        verbose_name_plural = verbose_name

    question_type = (
        (1, '单选题'),
        (2, '多选题'),
        (3, '判断题'),
    )

    exam_name = models.CharField('试卷名称', max_length=1024, default='无')
    exam_type = models.IntegerField('试题类型', choices=question_type)
    exam_score = models.IntegerField('试卷总分', default=4)  # 需要通过后台计算(可以使用 Ajax 动态计算)
    exam_count = models.IntegerField('试卷张数', default=60)
    exam_class = models.IntegerField('试卷类别个数', default=1)  # 设置有多少种不同的试卷  

    exam_single = models.IntegerField('单选题个数', default=1)
    exam_multiple = models.IntegerField('多选题个数', default=1)
    exam_judge = models.IntegerField('判断题个数', default=1)

    exam_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    exam_start_time = models.DateTimeField('开始时间', auto_now_add=True)
    exam_end_time = models.DateTimeField('结束时间', auto_now_add=True)
    exam_long = models.IntegerField('考试时长(单位h)', default=2)  # 单位h

    # 设置外键: 试卷属于哪个课程
    exam_fk_course = models.ForeignKey(verbose_name='课程', to=Course, on_delete=models.CASCADE)

    # 设置多对多关系: 试卷属于哪个人员
    exam_user = models.ManyToManyField(verbose_name="考生", to=User, null=True, blank=True)

    def __str__(self):
        return self.exam_name 
    


class Score(models.Model):
    """ 考试得分模型表 """
    class Meta:
        db_table = 'tb_score'  # 模型映射到数据库名称
        verbose_name = "考试成绩"
        verbose_name_plural = verbose_name

    score_score = models.IntegerField('考试分数', default=4)
    score_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    score_start_time = models.DateTimeField('开始时间', auto_now_add=True)
    score_end_time = models.DateTimeField('结束时间', auto_now_add=True)
    score_long = models.IntegerField('考试时长(单位h)', default=2)  # 单位h

    # 设置多对多: 试卷属于哪个课程
    score_exam = models.ManyToManyField(verbose_name='试卷', to=Exams, null=True, blank=True)

    # 设置多对多关系: 试卷属于哪个人员
    score_user = models.ForeignKey(verbose_name="考生", to=User, null=True, blank=True)

    def __str__(self):
        return self.score_score 
    

