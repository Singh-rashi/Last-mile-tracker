from models import Zone, RateCard, User


def calculate_delivery_charge(L, B, H, actual_weight, pickup_pin, drop_pin, order_type, payment_type):

    volumetric_weight = (L * B * H) / 5000
    billable_weight = max(actual_weight, volumetric_weight)


    pickup_zone = Zone.query.filter(Zone.pincodes.contains(pickup_pin)).first()
    drop_zone = Zone.query.filter(Zone.pincodes.contains(drop_pin)).first()

    is_intra = (pickup_zone.id == drop_zone.id) if (pickup_zone and drop_zone) else False


    rate_card = RateCard.query.filter_by(order_type=order_type).first()
    base_rate = rate_card.intra_zone_rate if is_intra else rate_card.inter_zone_rate

    total_charge = billable_weight * base_rate


    if payment_type == 'COD':
        total_charge += rate_card.cod_surcharge

    return round(total_charge, 2), volumetric_weight


def auto_assign_agent(pickup_pin):
   
    zone = Zone.query.filter(Zone.pincodes.contains(pickup_pin)).first()
    if zone:
        agent = User.query.filter_by(role='agent', zone_id=zone.id).first()
        return agent.id if agent else None
    return None