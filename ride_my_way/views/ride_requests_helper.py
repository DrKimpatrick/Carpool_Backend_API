def reaction_status(status):
    """
        Provides the value to be stored in the database
        Is called in a view function where driver
        accepts or rejects a ride request
    """
    # changing the status of a request
    if status == 'reject':
        status = 'rejected'
    if status == 'accept':
        status = 'accepted'
    if status == 'pending':
        status = 'pending'

    return status
