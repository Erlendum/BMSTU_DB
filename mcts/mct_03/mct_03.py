from playhouse.db_url import connect
from playhouse.shortcuts import Cast
import peewee as pw


db = connect("postgresext://erlendum:parasha@localhost:5431/RK3")


class BaseModel(pw.Model):
    class Meta:
        database = db


class Employees(BaseModel):
    employee_id = pw.PrimaryKeyField()
    employee_fio = pw.CharField()
    employee_birth_date = pw.DateField()
    employee_dep = pw.CharField()


class Ins_outs(BaseModel):
    employee_id = pw.ForeignKeyField(Employees, on_delete="cascade")
    ins_outs_date = pw.DateField()
    ins_outs_date = pw.CharField()
    ins_outs_time = pw.TimeField()
    ins_outs_type = pw.IntegerField()


# Найти самого старшего сотрудника в бухгалтерии
def task_01():
    print('TASK 01')
    cursor = db.execute_sql(" \
        select employee_fio, employee_birth_date\
	from employees\
	where employee_dep = 'Бухгалтерия' AND employee_birth_date =\
	(select min(employee_birth_date)\
	from employees\
	where employee_dep = 'Бухгалтерия');")
    for row in cursor.fetchall():
        print(row)
        
    min_birth_date = (Employees\
        .select(pw.fn.min(Employees.employee_birth_date).alias('mb'))\
        .where(Employees.employee_dep == 'Бухгалтерия'))

    query = Employees\
        .select(Employees.employee_fio, Employees.employee_birth_date)\
        .where(Employees.employee_dep=='Бухгалтерия' and Employees.employee_birth_date == min_birth_date)

    query = query.dicts().execute()
    for row in query:
        print(row)

# Найти сотрудников, выходивших более 3-х раз с рабочего места
def task_02():
    print('TASK 02')
    cursor = db.execute_sql(" \
        select employee_fio, cnt \
	from employees e join \
	(select distinct employee_id, count(*) as cnt \
	from ins_outs \
	where ins_outs_type = 2 \
	group by employee_id, ins_outs_date \
	having count(*) > 3) as tmp\
	on e.employee_id = tmp.employee_id;")
    for row in cursor.fetchall():
        print(row)
    Ins_outs1 = Ins_outs.alias()
    query = Ins_outs1\
        .select(Ins_outs1.employee_id, pw.fn.count(Ins_outs1.employee_id).alias('cnt')).distinct()\
        .where(Ins_outs1.ins_outs_type == 2)\
        .group_by(Ins_outs1.employee_id, Ins_outs1.ins_outs_date)\
        .having(pw.fn.count(Ins_outs1.employee_id) > 3)


    query1 = Employees.select( Employees.employee_fio, query.c.cnt).join(query, on=(query.c.employee_id==Employees.employee_id))
    query1 = query1.dicts().execute()
    for row in query1:
        print(row)
        
# Найти сотрудника, который пришёл сегодня последним
def task_03():
    print('TASK 03')
    cursor = db.execute_sql(" \
        with first_time_in as (\
	select distinct on (ins_outs_date, time_in) employee_id, ins_outs_date, min(ins_outs_time) OVER (PARTITION BY employee_id, ins_outs_date) as time_in\
	from ins_outs\
	where ins_outs_type = 1)\
        select e.employee_id, e.employee_fio, time_in \
	from first_time_in join employees e on first_time_in.employee_id = e.employee_id \
	where ins_outs_date = '2018-12-14' and time_in = (select max(time_in) \
	from first_time_in where ins_outs_date = '2018-12-14')")
    for row in cursor.fetchall():
        print(row)
    my_date = '2018-12-14'
    
    Ins_outs1 = Ins_outs.alias()
    query = Ins_outs1\
        .select(Ins_outs1.employee_id, Ins_outs1.ins_outs_date,
                pw.fn.min(Ins_outs1.ins_outs_time)\
                    .over(partition_by=[Ins_outs1.employee_id, Ins_outs1.ins_outs_date]).alias('time_in'))\
        .where(Ins_outs1.ins_outs_type == 1)\
        .where(Ins_outs1.ins_outs_date == my_date)\
        .order_by(pw.SQL('time_in').desc())\
        .distinct()\
        .limit(1)
    
    query1 = Employees.select(Employees.employee_fio, query.c.time_in).join(query, on=(query.c.employee_id==Employees.employee_id))
    query1 = query1.dicts().execute()
    for row in query1:
        print(row)
        
        
def main():
    task_01()
    task_02()
    task_03()


if __name__ == "__main__":
    main()
