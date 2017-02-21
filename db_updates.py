def rescue_fetcher(rescue_id):

    rescue_details = db.session.query(Rescue.rescue_id,
                                      Rescue.name,
                                      Rescue.phone,
                                      Rescue.address,
                                      Rescue.email,
                                      Rescue.img_url).filter(
                                      Rescue.rescue_id == rescue_id).first()
    return rescue_details