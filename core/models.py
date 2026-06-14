# from datetime import timezone
# import hashlib
# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     ROLES = (
#         ('CUSTOMER', 'Customer'),
#         ('RETAILER', 'Retailer'),
#         ('MANUFACTURER', 'Manufacturer'),
#         ('DISTRIBUTOR', 'Distributor'),
#         ('ADMIN', 'Admin')
#     )
#     role = models.CharField(max_length=20, choices=ROLES)
#     phone = models.CharField(max_length=15, null=True, blank=True)

# class SiteConfig(models.Model):
#     logo = models.ImageField(upload_to='site/')
#     site_name = models.CharField(max_length=100)

# class HomeSlider(models.Model):
#     image = models.ImageField(upload_to='slider/')
#     caption = models.CharField(max_length=200)
#     is_active = models.BooleanField(default=True)

# class ManufacturerProduct(models.Model):
#     manufacturer = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='products/')
#     base_price = models.DecimalField(max_digits=10, decimal_places=2)
#     min_quantity = models.PositiveIntegerField()
#     available_quantity = models.PositiveIntegerField()  # 🔧 CONFIRMED


# class DistributorStock(models.Model):
#     distributor = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(ManufacturerProduct, on_delete=models.CASCADE)  # 🔧 CONFIRMED
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     available_quantity = models.PositiveIntegerField()
#     transaction_id = models.CharField(max_length=100, unique=True , null=True)

# class RetailerStock(models.Model):
#     retailer = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(DistributorStock, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     available_quantity = models.PositiveIntegerField()
#     transaction_id = models.CharField(max_length=100, unique=True ,null=True)

# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(RetailerStock, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     order_date = models.DateTimeField(auto_now_add=True)




# class Transaction(models.Model):
#     transaction_id = models.CharField(max_length=100, unique=True)
#     product = models.ForeignKey(RetailerStock, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     customer = models.ForeignKey(User, related_name='customer_transactions', on_delete=models.CASCADE)
#     retailer = models.ForeignKey(User, related_name='retailer_transactions', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

# class Transaction(models.Model):
#     CHAIN_TYPES = (
#         ('CUSTOMER', 'Customer Transaction'),
#         ('DISTRIBUTOR', 'Distributor Transaction'),
#     )
    
#     transaction_id = models.CharField(max_length=100, unique=True)
#     product = models.ForeignKey(RetailerStock, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     customer = models.ForeignKey(
#         User, 
#         related_name='customer_transactions', 
#         on_delete=models.CASCADE,
#         null=True,  # Allow null for distributor transactions
#         blank=True
#     )
#     retailer = models.ForeignKey(
#         User, 
#         related_name='retailer_transactions', 
#         on_delete=models.CASCADE,
#         null=True,  # Allow null for distributor transactions
#         blank=True
#     )
#     distributor = models.ForeignKey(
#         User,
#         related_name='distributor_transactions',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True
#     )
#     chain_type = models.CharField(
#         max_length=20, 
#         choices=CHAIN_TYPES, 
#         default='CUSTOMER'
#     )
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.chain_type} - {self.transaction_id}"

#     def is_distributor_transaction(self):
#         return self.chain_type == 'DISTRIBUTOR'



# class Transaction(models.Model):
#     CHAIN_TYPES = (
#         ('CUSTOMER', 'Customer Transaction'),
#         ('DISTRIBUTOR', 'Distributor Transaction'),
#     )
    
#     transaction_id = models.CharField(max_length=100, unique=True)
#     product = models.ForeignKey(RetailerStock, on_delete=models.CASCADE, null=True, blank=True)  # For customer transactions
#     manu_product = models.ForeignKey(ManufacturerProduct, on_delete=models.CASCADE, null=True, blank=True)  # For distributor transactions
#     quantity = models.PositiveIntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     customer = models.ForeignKey(
#         User, 
#         related_name='customer_transactions', 
#         on_delete=models.CASCADE,
#         null=True,  # Allow null for distributor transactions
#         blank=True
#     )
#     retailer = models.ForeignKey(
#         User, 
#         related_name='retailer_transactions', 
#         on_delete=models.CASCADE,
#         null=True,  # Allow null for distributor transactions
#         blank=True
#     )
#     chain_type = models.CharField(max_length=20, choices=CHAIN_TYPES, default='CUSTOMER')
#     timestamp = models.DateTimeField(auto_now_add=True)

# # Block Model
# class Block(models.Model):
#     CHAIN_TYPES = (
#         ('CUSTOMER', 'Customer Transactions'),
#         ('DISTRIBUTOR', 'Distributor Transactions'),
#     )
    
#     chain_type = models.CharField(max_length=20, choices=CHAIN_TYPES, default='CUSTOMER')
#     index = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     # transactions = models.ManyToManyField(Transaction)
#     transactions = models.ManyToManyField(Transaction) 
#     previous_hash = models.CharField(max_length=64)
#     proof = models.IntegerField()

#     @property
#     def hash(self):
#         return hashlib.sha256(
#             f"{self.chain_type}{self.index}{self.timestamp}{self.proof}".encode()
#         ).hexdigest()

# class Block(models.Model):
#     index = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     transactions = models.ManyToManyField(Transaction)
#     previous_hash = models.CharField(max_length=64)
#     proof = models.IntegerField()

#     @property
#     def hash(self):
#         return hashlib.sha256(f"{self.index}{self.timestamp}{self.proof}".encode()).hexdigest()

# class Block(models.Model):
#     CHAIN_TYPES = (
#         ('CUSTOMER', 'Customer Transactions'),
#         ('DISTRIBUTOR', 'Distributor Transactions'),
#     )
#     chain_type = models.CharField(
#         max_length=20, 
#         choices=CHAIN_TYPES, 
#         default='CUSTOMER'  # Maintains existing behavior
#     )
#     index = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     transactions = models.ManyToManyField(Transaction)
#     previous_hash = models.CharField(max_length=64)
#     proof = models.IntegerField()

#     @property
#     def hash(self):
#         # Include chain_type in hash calculation for chain separation
#         return hashlib.sha256(
#             f"{self.chain_type}{self.index}{self.timestamp}{self.proof}".encode()
#         ).hexdigest()


# def new_block(self, proof):
#     previous_hash = self.hash(self.last_block) if self.last_block else '1'
#     block = Block.objects.create(
#         index=len(self.chain) + 1,
#         proof=proof,
#         previous_hash=previous_hash,
#         timestamp=timezone.now()
#     )
#     block.transactions.set(self.current_transactions)
#     self.current_transactions = []
#     self.chain.append(block)
#     return block



# def new_block(self, proof, chain_type='CUSTOMER'):
#     # Get previous hash based on chain type
#     last_block_same_chain = Block.objects.filter(chain_type=chain_type).order_by('-index').first()
#     previous_hash = self.hash(last_block_same_chain) if last_block_same_chain else '1'
    
#     # Create new block with chain type
#     block = Block.objects.create(
#         index=Block.objects.filter(chain_type=chain_type).count() + 1,
#         proof=proof,
#         previous_hash=previous_hash,
#         chain_type=chain_type,
#         timestamp=timezone.now()
#     )
    
#     # Filter transactions by chain type before adding to block
#     filtered_transactions = [
#         tx for tx in self.current_transactions 
#         if tx.chain_type == chain_type
#     ]
    
#     block.transactions.set(filtered_transactions)
#     self.current_transactions = []
    
#     # Maintain in-memory chain for current session
#     self.chain.append(block)
#     return block



from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib
from datetime import timezone

class User(AbstractUser):
    ROLES = (
        ('CUSTOMER', 'Customer'),
        ('RETAILER', 'Retailer'),
        ('MANUFACTURER', 'Manufacturer'),
        ('DISTRIBUTOR', 'Distributor'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    upi_qr_code = models.ImageField(upload_to='user_upi_qr_codes/', null=True, blank=True)  # New field for UPI QR code

# ======================================
# Supply Chain Models
# ======================================
class SiteConfig(models.Model):
    logo = models.ImageField(upload_to='site/')
    site_name = models.CharField(max_length=100)

class HomeSlider(models.Model):
    image = models.ImageField(upload_to='slider/')
    caption = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

class ManufacturerProduct(models.Model):
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()

class DistributorStock(models.Model):
    distributor = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ManufacturerProduct, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    transaction_id = models.CharField(max_length=100, unique=True, null=True)

class RetailerStock(models.Model):
    retailer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(DistributorStock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    transaction_id = models.CharField(max_length=100, unique=True, null=True)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(RetailerStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

# ======================================
# Blockchain Models
# ======================================
class Transaction(models.Model):
    CHAIN_TYPES = (
        ('CUSTOMER', 'Customer Transaction'),
        ('DISTRIBUTOR', 'Distributor Transaction')
    )
    
    transaction_id = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(RetailerStock, on_delete=models.CASCADE, null=True, blank=True)  # Customer transactions
    manu_product = models.ForeignKey(ManufacturerProduct, on_delete=models.CASCADE, null=True, blank=True)  # Distributor transactions
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(
        User,
        related_name='customer_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    retailer = models.ForeignKey(
        User,
        related_name='retailer_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    chain_type = models.CharField(max_length=20, choices=CHAIN_TYPES, default='CUSTOMER')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chain_type} - {self.transaction_id}"

    def is_distributor_transaction(self):
        return self.chain_type == 'DISTRIBUTOR'

class Block(models.Model):
    CHAIN_TYPES = (
        ('CUSTOMER', 'Customer Transactions'),
        ('DISTRIBUTOR', 'Distributor Transactions')
    )
    chain_type = models.CharField(max_length=20, choices=CHAIN_TYPES, default='CUSTOMER')
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    transactions = models.ManyToManyField(Transaction)
    previous_hash = models.CharField(max_length=64)
    proof = models.IntegerField()

    @property
    def hash(self):
        return hashlib.sha256(
            f"{self.chain_type}{self.index}{self.timestamp}{self.proof}".encode()
        ).hexdigest()
