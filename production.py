from gurobipy import *
import numpy as np


regular_hour_A = 1800
regular_hour_B = 2720
products = ['Aileron', 'Elevon', 'Flap']
period = ['i', 'ii', 'iii', 'iv', 'v', 'vi']
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
    ('i', 'A'): 30.5,
    ('i', 'B'): 30.5,
    ('i', 'C'): 46,
    ('i', 'D'): 46,
    ('ii', 'A'): 30.5,
    ('ii', 'B'): 30.5,
    ('ii', 'C'): 46,
    ('ii', 'D'): 46,
    ('iii', 'A'): 32,
    ('iii', 'B'): 32,
    ('iii', 'C'): 48.2,
    ('iii', 'D'): 48.2,
    ('iv', 'A'): 33.5,
    ('iv', 'B'): 33.5,
    ('iv', 'C'): 46.0,
    ('iv', 'D'): 46.0,
    ('v', 'A'): 33.5,
    ('v', 'B'): 33.5,
    ('v', 'C'): 46.0,
    ('v', 'D'): 46.0,
    ('vi', 'A'): 33.5,
    ('vi', 'B'): 33.5,
    ('vi', 'C'): 46.0,
    ('vi', 'D'): 46.0,
}


material_cost = {
    ('type1', 'A'): 2.50,
    ('type1', 'B'): 2.90,
    ('type1', 'C'): 2.50,
    ('type1', 'D'): 2.90,
    ('type2', 'A'): 3.40,
    ('type2', 'B'): 5.70,
    ('type2', 'C'): 3.40,
    ('type2', 'D'): 5.70
}

shipping_cost = {
    ('Aileron', 'A'): 11.4,
    ('Aileron', 'B'): 12.20,
    ('Aileron', 'C'): 11.4,
    ('Aileron', 'D'): 12.20,
    ('Elevon', 'A'): 8.20,
    ('Elevon', 'B'): 8.80,
    ('Elevon', 'C'): 8.20,
    ('Elevon', 'D'): 8.80,
    ('Flap', 'A'): 9.70,
    ('Flap', 'B'): 10.20,
    ('Flap', 'C'): 9.70,
    ('Flap', 'D'): 10.20,
}



holding_cost = {
    ('Aileron'): 55.00,
    ('Elevon'): 47.60,
    ('Flap'): 60.00
}

requirements = {
    ('i', 'Aileron'): 65,
    ('i', 'Elevon'): 220,
    ('i', 'Flap'): 135,
    ('ii', 'Aileron'): 95,
    ('ii', 'Elevon'): 245,
    ('ii', 'Flap'): 170,
    ('iii', 'Aileron'): 135,
    ('iii', 'Elevon'): 245,
    ('iii', 'Flap'): 195,
    ('iv', 'Aileron'): 250,
    ('iv', 'Elevon'): 290,
    ('iv', 'Flap'): 160,
    ('v', 'Aileron'): 190,
    ('v', 'Elevon'): 310,
    ('v', 'Flap'): 210,
    ('vi', 'Aileron'): 210,
    ('vi', 'Elevon'): 200,
    ('vi', 'Flap'): 190,
}

advertising_cost = {
    'Aileron': 410,
    'Elevon': 310,
    'Flap': 440
}

material_requirements = {
    ('Aileron', 'type1', 'A'): 185,
    ('Aileron', 'type2', 'A'): 8.4,
    ('Aileron', 'labor', 'A'): 8.6,
    ('Elevon', 'type1', 'A'): 225.00,
    ('Elevon', 'type2', 'A'): 0.00,
    ('Elevon', 'labor', 'A'): 7.00,
    ('Flap', 'type1', 'A'): 170,
    ('Flap', 'type2', 'A'): 10.6,
    ('Flap', 'labor', 'A'): 10.20,
    ('Aileron', 'type1', 'B'): 180,
    ('Aileron', 'type2', 'B'): 8.2,
    ('Aileron', 'labor', 'B'): 8.2,
    ('Elevon', 'type1', 'B'): 220,
    ('Elevon', 'type2', 'B'): 0.00,
    ('Elevon', 'labor', 'B'): 6.9,
    ('Flap', 'type1', 'B'): 165,
    ('Flap', 'type2', 'B'): 9.8,
    ('Flap', 'labor', 'B'): 9.7,
    ('Aileron', 'type1', 'C'): 185,
    ('Aileron', 'type2', 'C'): 8.4,
    ('Aileron', 'labor', 'C'): 8.6,
    ('Elevon', 'type1', 'C'): 225.00,
    ('Elevon', 'type2', 'C'): 0.00,
    ('Elevon', 'labor', 'C'): 7.00,
    ('Flap', 'type1', 'C'): 170,
    ('Flap', 'type2', 'C'): 10.6,
    ('Flap', 'labor', 'C'): 10.20,
    ('Aileron', 'type1', 'D'): 180,
    ('Aileron', 'type2', 'D'): 8.2,
    ('Aileron', 'labor', 'D'): 8.2,
    ('Elevon', 'type1', 'D'): 220,
    ('Elevon', 'type2', 'D'): 0.00,
    ('Elevon', 'labor', 'D'): 6.9,
    ('Flap', 'type1', 'D'): 165,
    ('Flap', 'type2', 'D'): 9.8,
    ('Flap', 'labor', 'D'): 9.7,
}

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
        if i == 'i':
            temp = c[i, pro]
            obj += price[pro]*(requirements[i, pro] + temp)
        elif i == 'ii':
            temp1 = c[i, pro]
            obj += price[pro]*(requirements[i, pro] + temp1 + 0.4*temp)
        elif i == 'iii':
            temp2 = c[i, pro]
            obj+= price[pro]*(requirements[i, pro] + temp2 + 0.4*temp1 + 0.2*temp)
        elif i == 'iv':
            temp3 = c[i, pro]
            obj+= price[pro]*(requirements[i, pro] + temp3 + 0.4*temp2 + 0.2*temp1)
        elif i == 'v':
            temp4 = c[i, pro]
            obj+= price[pro]*(requirements[i, pro] + temp4 + 0.4*temp3 + 0.2*temp2)
        elif i == 'vi':
            temp5 = c[i, pro]
            obj+= price[pro]*(requirements[i, pro] + temp5 + 0.4*temp4 + 0.2*temp3)

#cost
for i in period:
    for j in products:
        for k in plant:
            for l in type:
                #labor cost
                if l == 'labor':
                    obj -= labor_cost[i, k]*material_requirements[j, l, k]*p[i, j, k]
                #material cost
                else:
                    obj -= material_cost[l, k]*material_requirements[j, l, k]*p[i, j, k]
            #holding cost + shipping cost
            obj -= shipping_cost[j, k]*ship[i, j, k] + sto[i, j, k]*holding_cost[j]
        #advertising cost
        obj -= c[i, j] * advertising_cost[j]



#Set objective
obj = m.setObjective(obj, GRB.MAXIMIZE)

#Add constraints:

#Labor constraints---regular hours
m.addConstrs(sum(p[i, j, 'A']*material_requirements[j, 'labor', 'A'] for j in products) <= regular_hour_A
             for i in period)

m.addConstrs(sum(p[i, j, 'B']*material_requirements[j, 'labor', 'B'] for j in products) <= regular_hour_B
             for i in period)


#period 2
m.addConstr(sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) >=
             0.95*sum(p['i', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) <=
             1.05*sum(p['i', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))


m.addConstr(sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) >=
             0.95*sum(p['i', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

m.addConstr(sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) <=
             1.05*sum(p['i', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

#period 3
m.addConstr(sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) >=
             0.95*sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) <=
             1.05*sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) >=
             0.95*sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

m.addConstr(sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) <=
             1.05*sum(p['ii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

#period 4
m.addConstr(sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) >=
             0.95*sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) <=
             1.05*sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) >=
             0.95*sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

m.addConstr(sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) <=
             1.05*sum(p['iii', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

#period 5
m.addConstr(sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) >=
             0.95*sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) <=
             1.05*sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) >=
             0.95*sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

m.addConstr(sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) <=
             1.05*sum(p['iv', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))


#period 6
m.addConstr(sum(p['vi', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) >=
             0.95*sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['vi', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']) <=
             1.05*sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['A', 'C']))

m.addConstr(sum(p['vi', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) >=
             0.95*sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

m.addConstr(sum(p['vi', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']) <=
             1.05*sum(p['v', j, k]*material_requirements[j, 'labor', k] for j in products for k in ['B', 'D']))

#material constraints
m.addConstrs(sum(material_requirements[j, 'type1', k]*p[i, j, k]
                 for k in plant for j in products) <= raw_material_A for i in period)

m.addConstrs(sum(material_requirements[j, 'type2', k]*p[i, j, k]
                 for k in plant for j in products) <= raw_material_B for i in period)

#storage and shipping constraints
m.addConstrs(sum(ship['i', j, k] for k in ['A', 'C']) <= sum(p['i', j, k] for k in ['A', 'C'])
             for j in products)

m.addConstrs(sum(ship['i', j, k] for k in ['B', 'D']) <= sum(p['i', j, k] for k in ['B', 'D'])
             for j in products)

m.addConstrs(sum(sto['i', j, k] for k in ['A', 'C']) == sum(p['i', j, k] for k in ['A', 'C'])
             - sum(ship['i', j, k] for k in ['A', 'C']) for j in products)

m.addConstrs(sum(sto['i', j, k] for k in ['B', 'D']) == sum(p['i', j, k] for k in ['B', 'D'])
             - sum(ship['i', j, k] for k in ['B', 'D']) for j in products)

m.addConstrs(sum(ship['i', j, k] for k in plant) == requirements['i', j] + c['i', j] for j in products)

m.addConstrs(sum(sto[i, j, k] for j in products for k in ['A', 'C']) <= storing_A for i in period)
m.addConstrs(sum(sto[i, j, k] for j in products for k in ['B', 'D']) <= storing_B for i in period)


#period 2
m.addConstrs(sum(ship['ii', j, k] for k in ['A', 'C']) <= sum(p['ii', j, k] + sto['i', j, k]
                                                              for k in ['A', 'C']) for j in products)

m.addConstrs(sum(ship['ii', j, k] for k in ['B', 'D']) <= sum(p['ii', j, k] + sto['i', j, k]
                                                              for k in ['B', 'D']) for j in products)



m.addConstrs(sum(sto['ii', j, k] for k in ['A', 'C']) == sum(p['ii', j, k] + sto['i', j, k] - ship['ii', j, k]
                                                              for k in ['A', 'C']) for j in products)

m.addConstrs(sum(sto['ii', j, k] for k in ['B', 'D']) == sum(p['ii', j, k] + sto['i', j, k] - ship['ii', j, k]
                                                              for k in ['B', 'D']) for j in products)

m.addConstrs(sum(ship['ii', j, k] for k in plant) == requirements['ii', j] + c['ii', j] + 0.4*c['i', j] for j in products)

#period 3
m.addConstrs(sum(ship['iii', j, k] for k in ['A', 'C']) <= sum(p['iii', j, k] + sto['ii', j, k]
                                                               for k in ['A', 'C']) for j in products)

m.addConstrs(sum(ship['iii', j, k] for k in ['B', 'D']) <= sum(p['iii', j, k] + sto['ii', j, k]
                                                               for k in ['B', 'D']) for j in products)

m.addConstrs(sum(sto['iii', j, k] for k in ['A', 'C']) == sum(p['iii', j, k] + sto['ii', j, k] - ship['iii', j, k]
                                                              for k in ['A', 'C']) for j in products)

m.addConstrs(sum(sto['iii', j, k] for k in ['B', 'D']) == sum(p['iii', j, k] + sto['ii', j, k] - ship['iii', j, k]
                                                              for k in ['B', 'D']) for j in products)

m.addConstrs(sum(ship['iii', j, k] for k in plant) == requirements['iii', j] + c['iii', j] + 0.4*c['ii', j] +
             0.2 * c['i', j] for j in products)

#period 4
m.addConstrs(sum(ship['iv', j, k] for k in ['A', 'C']) <= sum(p['iv', j, k] + sto['iii', j, k]
                                                               for k in ['A', 'C']) for j in products)

m.addConstrs(sum(ship['iv', j, k] for k in ['B', 'D']) <= sum(p['iv', j, k] + sto['iii', j, k]
                                                               for k in ['B', 'D']) for j in products)

m.addConstrs(sum(sto['iv', j, k] for k in ['A', 'C']) == sum(p['iv', j, k] + sto['iii', j, k] - ship['iv', j, k]
                                                              for k in ['A', 'C']) for j in products)

m.addConstrs(sum(sto['iv', j, k] for k in ['B', 'D']) == sum(p['iv', j, k] + sto['iii', j, k] - ship['iv', j, k]
                                                              for k in ['B', 'D']) for j in products)

m.addConstrs(sum(ship['iv', j, k] for k in plant) == requirements['iv', j] + c['iv', j] + 0.4*c['iii', j] +
             0.2 * c['ii', j] for j in products)

#period 5
m.addConstrs(sum(ship['v', j, k] for k in ['A', 'C']) <= sum(p['v', j, k] + sto['iv', j, k]
                                                               for k in ['A', 'C']) for j in products)

m.addConstrs(sum(ship['v', j, k] for k in ['B', 'D']) <= sum(p['v', j, k] + sto['iv', j, k]
                                                               for k in ['B', 'D']) for j in products)

m.addConstrs(sum(sto['v', j, k] for k in ['A', 'C']) == sum(p['v', j, k] + sto['iv', j, k] - ship['v', j, k]
                                                              for k in ['A', 'C']) for j in products)

m.addConstrs(sum(sto['v', j, k] for k in ['B', 'D']) == sum(p['v', j, k] + sto['iv', j, k] - ship['v', j, k]
                                                              for k in ['B', 'D']) for j in products)

m.addConstrs(sum(ship['v', j, k] for k in plant) == requirements['v', j] + c['v', j] + 0.4*c['iv', j] +
             0.2 * c['iii', j] for j in products)

#period 6
m.addConstrs(sum(ship['vi', j, k] for k in ['A', 'C']) <= sum(p['vi', j, k] + sto['v', j, k]
                                                               for k in ['A', 'C']) for j in products)

m.addConstrs(sum(ship['vi', j, k] for k in ['B', 'D']) <= sum(p['vi', j, k] + sto['v', j, k]
                                                               for k in ['B', 'D']) for j in products)

m.addConstrs(sum(sto['vi', j, k] for k in ['A', 'C']) == sum(p['vi', j, k] + sto['v', j, k] - ship['vi', j, k]
                                                              for k in ['A', 'C']) for j in products)

m.addConstrs(sum(sto['vi', j, k] for k in ['B', 'D']) == sum(p['vi', j, k] + sto['v', j, k] - ship['vi', j, k]
                                                              for k in ['B', 'D']) for j in products)

m.addConstrs(sum(ship['vi', j, k] for k in plant) == requirements['vi', j] + c['vi', j] + 0.4*c['v', j] +
             0.2 * c['iv', j] for j in products)

m.addConstr(sum(advertising_cost[j]*c[i, j] for i in period for j in products) <= total_invest_limit )


# m.Params.outputFlag = 0
m.optimize()
origObjVal = m.ObjVal
for v in m.getVars():
    print '%s %g' %(v.varName, v.x)
print 'Obj:',origObjVal

