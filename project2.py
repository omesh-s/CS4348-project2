"""Run the Project 2 bank simulation."""

from collections import deque
import random
import threading


TELLER_COUNT = 1
CUSTOMER_COUNT = 1


class Visit:
    """Shared data and signals for one customer and the assigned teller."""

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.teller_id = None
        self.transaction = None
        self.called = threading.Semaphore(0)
        self.introduced = threading.Semaphore(0)
        self.requested = threading.Semaphore(0)
        self.ordered = threading.Semaphore(0)
        self.finished = threading.Semaphore(0)
        self.left_teller = threading.Semaphore(0)


class Bank:
    def __init__(self):
        self.line = deque()
        self.line_lock = threading.Semaphore(1)
        self.output_lock = threading.Semaphore(1)
        self.customers_waiting = threading.Semaphore(0)
        self.closed = False

    def log(self, actor, message, partner=""):
        with self.output_lock:
            print(f"{actor} [{partner}]: {message}", flush=True)

    def serve(self, teller_id):
        teller = f"Teller {teller_id}"
        while True:
            self.log(teller, "ready to serve")
            self.log(teller, "waiting for a customer")
            self.customers_waiting.acquire()

            with self.line_lock:
                if self.closed:
                    break
                visit = self.line.popleft()
                customer = f"Customer {visit.customer_id}"
                visit.teller_id = teller_id
                self.log(teller, "calls customer from line", customer)
                visit.called.release()

            self.log(teller, "waiting for customer to approach", customer)
            visit.introduced.acquire()
            self.log(teller, "serving a customer", customer)
            self.log(teller, "asks for transaction", customer)
            self.log(teller, "waiting for transaction", customer)
            visit.requested.release()
            visit.ordered.acquire()

            transaction = visit.transaction
            self.log(teller, f"handling {transaction} transaction", customer)
            self.log(teller, f"finishes {transaction} transaction.", customer)
            self.log(teller, "wait for customer to leave.", customer)
            visit.finished.release()
            visit.left_teller.acquire()
            self.log(teller, "customer left teller", customer)

        self.log(teller, "leaving for the day")

    def visit(self, customer_id):
        visit = Visit(customer_id)
        customer = f"Customer {customer_id}"
        transaction = random.choice(("deposit", "withdrawal"))
        self.log(customer, f"wants to perform a {transaction} transaction")

        with self.line_lock:
            self.log(customer, "getting in line.")
            self.line.append(visit)
            self.log(customer, "waiting for a teller")
            self.customers_waiting.release()

        visit.called.acquire()
        teller = f"Teller {visit.teller_id}"
        self.log(customer, "selecting a teller.")
        self.log(customer, "selects teller", teller)
        self.log(customer, "introduces itself", teller)
        self.log(customer, "waiting for teller to ask for transaction", teller)
        visit.introduced.release()
        visit.requested.acquire()
        self.log(customer, "teller asked for transaction", teller)

        visit.transaction = transaction
        self.log(customer, f"asks for {transaction} transaction", teller)
        self.log(customer, "waiting for transaction to finish", teller)
        visit.ordered.release()
        visit.finished.acquire()
        self.log(customer, "transaction complete", teller)
        self.log(customer, "leaves teller", teller)
        visit.left_teller.release()

    def run(self):
        tellers = [
            threading.Thread(target=self.serve, args=(i,))
            for i in range(TELLER_COUNT)
        ]
        customers = [
            threading.Thread(target=self.visit, args=(i,))
            for i in range(CUSTOMER_COUNT)
        ]

        for teller in tellers:
            teller.start()
        for customer in customers:
            customer.start()
        for customer in customers:
            customer.join()

        with self.line_lock:
            self.closed = True
        for _ in tellers:
            self.customers_waiting.release()
        for teller in tellers:
            teller.join()
        print("The bank closes for the day.")


if __name__ == "__main__":
    Bank().run()
