from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import tbl_mobil as tbl_mobilModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'id': 4, 'harga': 3, 'rate': 5, 'ukuran': 3}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(tbl_mobilModel.nama_mobil, tbl_mobilModel.id, tbl_mobilModel.harga, tbl_mobilModel.rate, tbl_mobilModel.ukuran)
        result = session.execute(query).fetchall()
        print(result)
        return [{'nama_mobil': tbl_mobil.nama_mobil, 'id': tbl_mobil.id, 'harga': tbl_mobil.harga, 'rate': tbl_mobil.rate, 'ukuran': tbl_mobil.ukuran} for tbl_mobil in result]

    @property
    def normalized_data(self):
        id_values = []
        harga_values = []
        rate_values = []
        ukuran_values = []

        for data in self.data:
            id_values.append(data['id'])
            harga_values.append(data['harga'])
            rate_values.append(data['rate'])
            ukuran_values.append(data['ukuran'])

        return [
            {'nama_mobil': data['nama_mobil'],
             'id': min(id_values) / data['id'],
             'harga': data['harga'] / max(harga_values),
             'rate': data['rate'] / max(rate_values),
             'ukuran': data['ukuran'] / max(ukuran_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['id'] ** self.raw_weight['id'] *
                row['harga'] ** self.raw_weight['harga'] *
                row['rate'] ** self.raw_weight['rate'] *
                row['ukuran'] ** self.raw_weight['ukuran']
            )

            produk.append({
                'nama_mobil': row['nama_mobil'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'nama_mobil': product['nama_mobil'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['nama_mobil']:
                  round(row['id'] * weight['id'] +
                        row['harga'] * weight['harga'] +
                        row['rate'] * weight['rate'] +
                        row['ukuran'] * weight['ukuran'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class tbl_mobil(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(tbl_mobilModel)
        data = [{'nama_mobil': tbl_mobil.nama_mobil, 'id': tbl_mobil.id, 'harga': tbl_mobil.harga, 'rate': tbl_mobil.rate, 'ukuran': tbl_mobil.ukuran} for tbl_mobil in session.scalars(query)]
        return self.get_paginated_result('tbl_mobil/', data, request.args), HTTPStatus.OK.value


api.add_resource(tbl_mobil, '/tbl_mobil')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)