from flask import Flask, request, jsonify, render_template
from models import db, Order, User, Zone, RateCard, OrderHistory
from logic import calculate_delivery_charge, auto_assign_agent
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'delivery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()

    if not Zone.query.first():
        print("Initializing database with seed data...")
        z1 = Zone(name="North", pincodes="110001,110002")
        db.session.add(z1)
        db.session.commit()  # Commit zone first to get its ID

        rc = RateCard(order_type="B2C", intra_zone_rate=50, inter_zone_rate=100, cod_surcharge=20)
        admin = User(username="admin", role="admin")
        agent = User(username="agent1", role="agent", zone_id=z1.id)

        db.session.add_all([rc, admin, agent])
        db.session.commit()
        print("Database ready!")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    try:

        charge, vol_weight = calculate_delivery_charge(
            data['L'], data['B'], data['H'], data['weight'],
            data['pickup_pin'], data['drop_pin'], data['type'], data['payment']
        )

        new_order = Order(
            customer_id=data['user_id'],
            pickup_pincode=data['pickup_pin'],
            drop_pincode=data['drop_pin'],
            weight_actual=data['weight'],
            weight_volumetric=vol_weight,
            final_charge=charge,
            order_type=data['type'],
            payment_type=data['payment']
        )


        new_order.agent_id = auto_assign_agent(data['pickup_pin'])

        db.session.add(new_order)
        db.session.commit()

        # Initial History log
        log = OrderHistory(order_id=new_order.id, status="Order Created", updated_by="System")
        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Order placed", "order_id": new_order.id, "charge": charge})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    order = Order.query.get(data['order_id'])
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.status = data['status']


    log = OrderHistory(order_id=order.id, status=data['status'], updated_by=data['user_role'])
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": f"Status updated to {data['status']}"})


if __name__ == '__main__':
    app.run(debug=True)