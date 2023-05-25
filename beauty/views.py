from django.shortcuts import render, redirect
from django.db import connection
from beauty.beautyUtil import dictfetchall
from django.utils import timezone

# Create your views here.
def beauty_index(request):
    cursor = connection.cursor()

    sql = """
    select beauty.beauty_seq, beauty.mem_seq, beauty.beauty_name, beauty.beauty_hit, beauty.beauty_wdate, mem.mem_name
    from beautytaurant beauty join member mem
    on beauty.mem_seq = mem.mem_seq
    order by beauty.beauty_seq desc
    """

    cursor.execute(sql)
    resList = dictfetchall(cursor)
    return render(request, 'beauty/beauty_index.html', {'beauty_list':beautyList})

def beauty_detail(request, beauty_seq):
    cursor = connection.cursor()

    sql = f"""
    select beauty_name, beauty_locate, beauty_phone, beauty_content,  beauty_score, beauty_hit, beauty_wdate
    from beautytaurant
    where beauty_seq = {beauty_seq}
    """
    cursor.execute(sql)
    beautyInfo = dictfetchall(cursor)[0]

    
    sql = f"""
    select beauty_item_title, beauty_item_content, beauty_item_pic, beauty_item_price
    from beauty_item
    where beauty_seq = {beauty_seq}
    """
    cursor.execute(sql)
    menuList = dictfetchall(cursor)

    sql = f"""
    select mem.mem_id, rev.beauty_review_title, rev.beauty_review_content,
    rev.beauty_review_wdate, rev.beauty_review_rating
    from beauty_review rev join member mem
    on rev.beauty_seq = mem.beauty_seq
    where beauty_seq = {beauty_seq}

    """

    # sql = f"""
    # select B.mem_id, rev.beauty_review_title, rev.beauty_review_content,
    # rev.beauty_review_wdate, rev.beauty_review_rating
    # from beauty_review rev join
    #     (select beauty.beauty_seq, mem.mem_id
    #     from beautytaurant beauty join member mem
    #     on beauty.beauty_seq = mem.beauty_seq
    #     where beauty_seq = {beauty_seq}) B
    # on rev.beauty_seq = B.beauty_seq
    # """
    sql = f"""
    SELECT mem.mem_id, rev.beauty_review_title, rev.beauty_review_content,
    rev.beauty_review_wdate, rev.beauty_review_rating
    FROM beauty_review rev
        JOIN beautytaurant beauty
        ON rev.beauty_seq = beauty.beauty_seq
    INNER JOIN member mem
        ON beauty.mem_seq = mem.mem_seq
    where beauty.beauty_seq = {beauty_seq}
    """
    cursor.execute(sql)
    reviewList = dictfetchall(cursor)
    return render(request, 'beauty/beauty_detail.html',  
                  {'beautyInfo':beautyInfo, "menuList":menuList, 'reviewList':reviewList})

def beauty_join_form(request):
    return render(request, 'beauty/beauty_join_form.html')

def beauty_join_save(request):

    mem_id = request.POST.get('mem_id')
    password = request.POST.get('pwd')
    membertype = request.POST.get('membertype')
    age = request.POST.get('age')
    name = request.POST.get('name')
    cursor = connection.cursor()
    sql = f"""
    insert into member values(mem_req.NEXTVAL, '{mem_id}', '{password}', 'N', 'N', 1, {age}, '윤', sysdate, sysdate)
    """
    cursor.execute(sql)
    connection.commit()

    return redirect('beauty:main')

def main(request):
    return render(request, 'beauty/beauty_main.html')

def write(request):
    return render(request, 'beauty/beauty_write.html')