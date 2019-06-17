from autoLoad import *
import uuid
import random
import string


class booking:

    ## Intiatlizing booking, storing passenger details, Locking the seats
    def initBooking(self, selectedFlighDetails, inputData, passengerCnt):
        try:
            pnrNumber = ""
            stringLength = PNRLENGTH
            pnrNumber = uuid.uuid4().hex  # get a random string in a UUID fromat
            pnrNumber = pnrNumber.upper()[0:stringLength]  # convert it in a uppercase letter and trim to your size.

            flight_id = selectedFlighDetails['flid']
            amount_usd = str(selectedFlighDetails['base_price_usd'])
            queryStr = "insert into flight_booking(pnr, flight_id, amount_usd, no_passenger) values(%s, %s, %s, %s)"
            queryVal = (pnrNumber, flight_id, amount_usd, passengerCnt)
            result = DBActivity.db.insert(queryStr, queryVal)
            if result['count'] in [-1]:
                DBActivity.db.transactRollback()
                print("Booking Failed, Please try again ")
                sys.exit()
            ## Inserting Passenger details
            for passenger in inputData:
                ## manually selecting the Seat Number
                seat_number = random.choice(string.ascii_letters) + str(random.randint(1, 7))
                insertVal = (pnrNumber, seat_number, passenger["first_name"], passenger["middle_name"], passenger["last_name"],
                               passenger["date_of_birth"], passenger["gender"], passenger["email"],
                               passenger["phone"], passenger["is_primary"])
                insertStr = "insert into flight_booking_passenger(pnr, seat_number, first_name, middle_name, last_name, " \
                            "date_of_birth, gender, email, phone, is_primary)" \
                            " values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                insertResult = DBActivity.db.insert(insertStr, insertVal)
                if insertResult['count'] in [-1]:
                    DBActivity.db.transactRollback()
                    print("Booking Failed, Please try again ")
                    sys.exit()


            ## Reducing the seat availability count
            updateStr = "update flights set available_seats = (available_seats-%s) where flid = %s"
            updateVal = ((passengerCnt, flight_id))
            updateResult = DBActivity.db.update(updateStr, updateVal)
            if updateResult['count'] in [-1]:
                DBActivity.db.transactRollback()
                print("Booking Failed, Please try again ")
                sys.exit()

            ## Since there is no Payment process involved, updating Txn as Completed
            updateTxnStr = "update flight_booking set `txn_status` = 'completed', `payment_status` = 'completed' " \
                           "where pnr = %s"
            updateTxnVal = ((pnrNumber,))
            updateTxnResult = DBActivity.db.update(updateTxnStr, updateTxnVal)
            if updateTxnResult['count'] in [-1]:
                DBActivity.db.transactRollback()
                print(updateTxnResult)
                print("Booking Txn Failed, Please try again ")
                sys.exit()

            bookingResult = DBActivity.db.transctionCommit()
            if bookingResult['count'] not in [-1, 0]:
               print("Booking is Successfull, Your PNR is:" + pnrNumber)
            else:
                print("Booking Failes, Please try again ")
                sys.exit()


        except mysqlDB.Error as err:
            print("Something went wrong: {}".format(err))





