from gurobipy import *
"""
use integer programming to solve 6 periods production decision problem with gurobi
in the case we have labor hourconstraint, reliability constraint, dynamic labor cost,
raw material constraint, storing, shipping constraints and advertising budget constraints
demands created by advertisements are dynamic
for more detail about the problem, see the files I attached"""

regular_hour_A = 1800
regular_hour_B = 2720
hour_limit = {
    'A': 1800,
    'B': 2720}

products = ['Aileron', 'Elevon', 'Flap']
period = [0, 1, 2, 3, 4, 5]
plant = ['A', 'B', 'C', 'D']
type = ['type1', 'type2', 'labor']
raw_material_A = 150000
raw_material_B = 4100
storing_A = 42
storing_B = 56
total_invest_limit = 140000

price = {
    'Aileron': 5500,
    'Elevon': 4860,
    'Flap': 5850}

labor_cost = {
    (0, 'A'): 30.5, (0, 'B'): 30.5, (0, 'C'): 46, (0, 'D'): 46,
    (1, 'A'): 30.5, (1, 'B'): 30.5, (1, 'C'): 46, (1, 'D'): 46,
    (2, 'A'): 32, (2, 'B'): 32, (2, 'C'): 48.2, (2, 'D'): 48.2,
    (3, 'A'): 33.5, (3, 'B'): 33.5, (3, 'C'): 46.0, (3, 'D'): 46.0,
    (4, 'A'): 33.5, (4, 'B'): 33.5, (4, 'C'): 46.0, (4, 'D'): 46.0,
    (5, 'A'): 33.5, (5, 'B'): 33.5, (5, 'C'): 46.0, (5, 'D'): 46.0}

material_cost = {
    ('type1', 'A'): 2.50, ('type1', 'B'): 2.90, ('type1', 'C'): 2.50, ('type1', 'D'): 2.90,
    ('type2', 'A'): 3.40, ('type2', 'B'): 5.70, ('type2', 'C'): 3.40, ('type2', 'D'): 5.70}

shipping_cost = {
    ('Aileron', 'A'): 11.4, ('Aileron', 'B'): 12.20, ('Aileron', 'C'): 11.4, ('Aileron', 'D'): 12.20,
    ('Elevon', 'A'): 8.20, ('Elevon', 'B'): 8.80, ('Elevon', 'C'): 8.20, ('Elevon', 'D'): 8.80,
    ('Flap', 'A'): 9.70, ('Flap', 'B'): 10.20, ('Flap', 'C'): 9.70, ('Flap', 'D'): 10.20}

holding_cost = {'Aileron': 55.00, 'Elevon': 47.60, 'Flap': 60.00}

requirements = {
    (0, 'Aileron'): 65, (0, 'Elevon'): 220, (0, 'Flap'): 135,
    (1, 'Aileron'): 95, (1, 'Elevon'): 245, (1, 'Flap'): 170,
    (2, 'Aileron'): 135, (2, 'Elevon'): 245, (2, 'Flap'): 195,
    (3, 'Aileron'): 250, (3, 'Elevon'): 290, (3, 'Flap'): 160,
    (4, 'Aileron'): 190, (4, 'Elevon'): 310, (4, 'Flap'): 210,
    (5, 'Aileron'): 210, (5, 'Elevon'): 200, (5, 'Flap'): 190}

advertising_cost = {
    'Aileron': 410, 'Elevon': 310, 'Flap': 440}

material_requirements = {
    ('Aileron', 'type1', 'A'): 185, ('Aileron', 'type2', 'A'): 8.4, ('Aileron', 'labor', 'A'): 8.6,
    ('Elevon', 'type1', 'A'): 225.00, ('Elevon', 'type2', 'A'): 0.00, ('Elevon', 'labor', 'A'): 7.00,
    ('Flap', 'type1', 'A'): 170, ('Flap', 'type2', 'A'): 10.6, ('Flap', 'labor', 'A'): 10.20,
    ('Aileron', 'type1', 'B'): 180, ('Aileron', 'type2', 'B'): 8.2, ('Aileron', 'labor', 'B'): 8.2,
    ('Elevon', 'type1', 'B'): 220, ('Elevon', 'type2', 'B'): 0.00, ('Elevon', 'labor', 'B'): 6.9,
    ('Flap', 'type1', 'B'): 165, ('Flap', 'type2', 'B'): 9.8, ('Flap', 'labor', 'B'): 9.7,
    ('Aileron', 'type1', 'C'): 185, ('Aileron', 'type2', 'C'): 8.4, ('Aileron', 'labor', 'C'): 8.6,
    ('Elevon', 'type1', 'C'): 225.00, ('Elevon', 'type2', 'C'): 0.00, ('Elevon', 'labor', 'C'): 7.00,
    ('Flap', 'type1', 'C'): 170, ('Flap', 'type2', 'C'): 10.6, ('Flap', 'labor', 'C'): 10.20,
    ('Aileron', 'type1', 'D'): 180, ('Aileron', 'type2', 'D'): 8.2, ('Aileron', 'labor', 'D'): 8.2,
    ('Elevon', 'type1', 'D'): 220, ('Elevon', 'type2', 'D'): 0.00, ('Elevon', 'labor', 'D'): 6.9,
    ('Flap', 'type1', 'D'): 165, ('Flap', 'type2', 'D'): 9.8, ('Flap', 'labor', 'D'): 9.7,}

#create model
m = Model('dpp')

#variables period i produce product m in plant A
p = m.addVars(period, products, plant, vtype=GRB.INTEGER, name='production')

#products created by advertisement
c = m.addVars(period, products, vtype=GRB.INTEGER, name='advertisement')

#numer of products shipped in period i of products A from plant A
ship = m.addVars(period, products, plant, vtype=GRB.INTEGER, name='shippment')

#number of products stored in period i of products A from plant A
sto = m.addVars(period, products, plant, vtype=GRB.INTEGER, name='storage')

# total revenue
obj = 0
for pro in products:
    for i in period:
        if i == 0:
            obj += price[pro]*(requirements[i, pro] + c[i, pro])
        elif i == 1:
            obj += price[pro]*(requirements[i, pro] + c[i, pro] + 0.4*c[i-1, pro])
        else:
            obj+= price[pro]*(requirements[i, pro] + c[i, pro] + 0.4*c[i-1, pro] + 0.2*c[i-2, pro])

#labor, material, holding, shipping and advertising cost
for i in period:
    for j in products:
        for k in plant:
            for l in type:
                if l == 'labor':
                    obj -= labor_cost[i, k]*material_requirements[j, l, k]*p[i, j, k]#labor cost
                else:
                    obj -= material_cost[l, k]*material_requirements[j, l, k]*p[i, j, k]#material cost
            obj -= shipping_cost[j, k]*ship[i, j, k] + sto[i, j, k]*holding_cost[j]#holding cost + shipping cost
        obj -= c[i, j] * advertising_cost[j]#advertising cost

#Set objective: total revenue - toal cost
obj = m.setObjective(obj, GRB.MAXIMIZE)

#Add constraints:
#Labor constraints---regular hours
m.addConstrs(sum(p[i, j, k]*material_requirements[j, 'labor', k] for j in products) <= hour_limit[k]
             for i in period for k in ['A', 'B'])
#Labor reliablity
for i in period:
    if i ==5:
        break
    m.addConstr(sum(p[i+1, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) >=
                0.95*sum(p[i, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

    m.addConstr(sum(p[i+1, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) <=
                1.05*sum(p[i, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

    m.addConstr(sum(p[i+1, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) >=
                0.95*sum(p[i, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

    m.addConstr(sum(p[i+1, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) <=
                1.05*sum(p[i, j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

#material constraints
m.addConstrs(sum(material_requirements[j, 'type1', k]*p[i, j, k]
                 for k in plant for j in products) <= raw_material_A for i in period)

m.addConstrs(sum(material_requirements[j, 'type2', k]*p[i, j, k]
                 for k in plant for j in products) <= raw_material_B for i in period)

#storage and shipping constraints for 6 periods
for i in period:
    if i == 0:
        m.addConstrs(sum(ship[i, j, k] for k in ['A', 'C']) <= sum(p[i, j, k] for k in ['A', 'C'])
                     for j in products)

        m.addConstrs(sum(ship[i, j, k] for k in ['B', 'D']) <= sum(p[i, j, k] for k in ['B', 'D'])
                     for j in products)

        m.addConstrs(sum(sto[i, j, k] for k in ['A', 'C']) == sum(p[i, j, k] for k in ['A', 'C'])
                     - sum(ship[i, j, k] for k in ['A', 'C']) for j in products)

        m.addConstrs(sum(sto[i, j, k] for k in ['B', 'D']) == sum(p[i, j, k] for k in ['B', 'D'])
                     - sum(ship[i, j, k] for k in ['B', 'D']) for j in products)

        m.addConstrs(sum(ship[i, j, k] for k in plant) == requirements[i, j] + c[i, j] for j in products)

        m.addConstrs(sum(sto[i, j, k] for j in products for k in ['A', 'C']) <= storing_A for i in period)
        m.addConstrs(sum(sto[i, j, k] for j in products for k in ['B', 'D']) <= storing_B for i in period)

    elif i == 1:
        #period 2
        m.addConstrs(sum(ship[i, j, k] for k in ['A', 'C']) <= sum(p[i, j, k] + sto[i-1, j, k]
                                                                      for k in ['A', 'C']) for j in products)

        m.addConstrs(sum(ship[i, j, k] for k in ['B', 'D']) <= sum(p[i, j, k] + sto[i-1, j, k]
                                                                      for k in ['B', 'D']) for j in products)

        m.addConstrs(sum(sto[i, j, k] for k in ['A', 'C']) == sum(p[i, j, k] + sto[i-1, j, k] - ship[i, j, k]
                                                                      for k in ['A', 'C']) for j in products)

        m.addConstrs(sum(sto[i, j, k] for k in ['B', 'D']) == sum(p[i, j, k] + sto[i-1, j, k] - ship[i, j, k]
                                                                      for k in ['B', 'D']) for j in products)

        m.addConstrs(sum(ship[i, j, k] for k in plant) == requirements[i, j] + c[i, j] + 0.4*c[i-1, j] for j in products)
    else:
        #period 3,4,5,6
        m.addConstrs(sum(ship[i, j, k] for k in ['A', 'C']) <= sum(p[i, j, k] + sto[i-1, j, k]
                                                                       for k in ['A', 'C']) for j in products)

        m.addConstrs(sum(ship[i, j, k] for k in ['B', 'D']) <= sum(p[i, j, k] + sto[i-1, j, k]
                                                                       for k in ['B', 'D']) for j in products)

        m.addConstrs(sum(sto[i, j, k] for k in ['A', 'C']) == sum(p[i, j, k] + sto[i-1, j, k] - ship[i, j, k]
                                                                      for k in ['A', 'C']) for j in products)

        m.addConstrs(sum(sto[i, j, k] for k in ['B', 'D']) == sum(p[i, j, k] + sto[i-1, j, k] - ship[i, j, k]
                                                                      for k in ['B', 'D']) for j in products)

        m.addConstrs(sum(ship[i, j, k] for k in plant) == requirements[i, j] + c[i, j] + 0.4*c[i-1, j] +
                     0.2 * c[i-2, j] for j in products)

#advertising costs for 6 periods
m.addConstr(sum(advertising_cost[j]*c[i, j] for i in period for j in products) <= total_invest_limit )


# m.Params.outputFlag = 0
m.optimize()
origObjVal = m.ObjVal
for v in m.getVars():
    print '%s %g' %(v.varName, v.x)
print 'Obj:',origObjVal

