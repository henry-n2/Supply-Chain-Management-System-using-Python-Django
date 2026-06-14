from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test

# # @login_required
# def home(request):
#     sliders = HomeSlider.objects.filter(is_active=True)
#     site_config = SiteConfig.objects.first()
#     products = RetailerStock.objects.all()

#     # blocks_with_transactions = Block.objects.prefetch_related('transactions')

#     # transactions = Transaction.objects.filter(customer=request.user).select_related(
#     #     'product__product__product', 'retailer'
#     # ).prefetch_related(
#     #     Prefetch('block_set', queryset=blocks_with_transactions, to_attr='blocks')
#     # ).order_by('-timestamp')

#     return render(request, 'core/home.html', {
#         'sliders': sliders,
#         'site_config': site_config,
#         'products': products,
#         # 'transactions': transactions,
#     })



def home(request):
    sliders = HomeSlider.objects.filter(is_active=True)
    site_config = SiteConfig.objects.first()
    products = RetailerStock.objects.filter(available_quantity__gt=0)
    
    # Initialize empty transactions queryset
    transactions = Transaction.objects.none()
    
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(
            customer=request.user  # Critical filter
        ).select_related(
            'product__product__product', 'retailer'
        ).order_by('-timestamp')

    return render(request, 'core/home.html', {
        'sliders': sliders,
        'site_config': site_config,
        'products': products,
        'transactions': transactions,  # Will be empty for anonymous users
    })

@login_required
def manufacturer_dashboard(request):
    products = ManufacturerProduct.objects.filter(manufacturer=request.user)
    return render(request, 'core/manufacturer_dashboard.html', {'products': products})

# @login_required
# @user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
# def distributor_dashboard(request):
#     # Products available from manufacturers
#     products = ManufacturerProduct.objects.filter(available_quantity__gt=0)
#     # Products this distributor has already added
#     my_stocks = DistributorStock.objects.filter(distributor=request.user)
#     return render(request, 'core/distributor_dashboard.html', {
#         'products': products,
#         'my_stocks': my_stocks,
#     })


# from django.db.models import Prefetch

# @login_required
# @user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
# def distributor_dashboard(request):
#      products = ManufacturerProduct.objects.filter(available_quantity__gt=0)
#      my_stocks = DistributorStock.objects.filter(distributor=request.user)
#      blocks_with_transactions = Block.objects.prefetch_related('transactions')
#      sales_transactions = Transaction.objects.filter(
#         retailer=request.user,
#         chain_type='DISTRIBUTOR'
#     ).select_related(
#         'product__product__product', 'customer'
#     ).prefetch_related(
#         Prefetch('block_set', queryset=blocks_with_transactions, to_attr='blocks')
#     ).order_by('-timestamp')
#      my_stocks = DistributorStock.objects.filter(distributor=request.user)
#      return render(request, 'core/distributor_dashboard.html', {
#         'products': products,
#         'my_stocks': my_stocks,
#         'sales_transactions': sales_transactions,
#     })
    

@login_required
@user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
def distributor_dashboard(request):
    # Existing sales transactions (distributor as seller)
    sales_transactions = Transaction.objects.filter(
        retailer=request.user,
        chain_type='DISTRIBUTOR'
    ).select_related(
        'product__product__product', 'customer'
    ).prefetch_related(
        Prefetch('block_set', queryset=Block.objects.prefetch_related('transactions'), to_attr='blocks')
    ).order_by('-timestamp')

    # New purchases transactions (distributor as buyer)
    purchases_transactions = Transaction.objects.filter(
        customer=request.user,  # Distributor as buyer
        chain_type='DISTRIBUTOR'
    ).select_related(
        'manu_product', 'retailer'  # Manufacturer as seller
    ).prefetch_related(
        Prefetch('block_set', queryset=Block.objects.prefetch_related('transactions'), to_attr='blocks')
    ).order_by('-timestamp')

    products = ManufacturerProduct.objects.filter(available_quantity__gt=0)
    my_stocks = DistributorStock.objects.filter(distributor=request.user)

    return render(request, 'core/distributor_dashboard.html', {
        'products': products,
        'my_stocks': my_stocks,
        'sales_transactions': sales_transactions,
        'purchases_transactions': purchases_transactions  # New
    })


from django.contrib.auth.decorators import login_required

from django.db.models import Prefetch

@login_required
def customer_dashboard(request):
    sliders = HomeSlider.objects.filter(is_active=True)
    products = RetailerStock.objects.filter(available_quantity__gt=0)
    
    # Prefetch blocks related to transactions for efficient access
    blocks_with_transactions = Block.objects.prefetch_related('transactions')
    
    # Fetch transactions for the logged-in customer
    transactions = Transaction.objects.filter(customer=request.user).select_related(
        'product__product__product', 'retailer'
    ).prefetch_related(
        Prefetch('block_set', queryset=blocks_with_transactions, to_attr='blocks')
    ).order_by('-timestamp')

    return render(request, 'core/customer_dashboard.html', {
        'sliders': sliders,
        'products': products,
        'transactions': transactions,
    })

from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test

# @login_required
# @user_passes_test(lambda u: u.role == 'RETAILER')
# def retailer_dashboard(request):
#     blocks_with_transactions = Block.objects.prefetch_related('transactions')

#     transactions = Transaction.objects.filter(retailer=request.user).select_related(
#         'customer', 'product__product__product'
#     ).prefetch_related(
#         Prefetch('block_set', queryset=blocks_with_transactions, to_attr='blocks')
#     ).order_by('-timestamp')

#     distributor_products = DistributorStock.objects.select_related('product', 'distributor').filter(available_quantity__gt=0)
#     my_stocks = RetailerStock.objects.filter(retailer=request.user)

#     return render(request, 'core/retailer_dashboard.html', {
#         'transactions': transactions,
#         'distributor_products': distributor_products,
#         'my_stocks': my_stocks,
#     })
# Fixed^
# @login_required
# @user_passes_test(lambda u: u.role == 'RETAILER')
# def retailer_dashboard(request):
#     # Customer transactions (sales)
#     customer_blocks = Block.objects.prefetch_related('transactions')
#     customer_transactions = Transaction.objects.filter(
#         retailer=request.user
#     ).select_related(
#         'customer', 'product__product__product'
#     ).prefetch_related(
#         Prefetch('block_set', queryset=customer_blocks, to_attr='blocks')
#     ).order_by('-timestamp')

#     # Distributor transactions (purchases)
#     distributor_blocks = Block.objects.prefetch_related('transactions')
#     distributor_transactions = Transaction.objects.filter(
#         customer=request.user  # Retailer as buyer
#     ).select_related(
#         'retailer',  # Points to distributor
#         'product__product__product'
#     ).prefetch_related(
#         Prefetch('block_set', queryset=distributor_blocks, to_attr='blocks')
#     ).order_by('-timestamp')

#     # Product listings
#     distributor_products = DistributorStock.objects.select_related('product', 'distributor').filter(
#         available_quantity__gt=0
#     )
#     my_stocks = RetailerStock.objects.filter(retailer=request.user)

#     return render(request, 'core/retailer_dashboard.html', {
#         'customer_transactions': customer_transactions,
#         'distributor_transactions': distributor_transactions,
#         'distributor_products': distributor_products,
#         'my_stocks': my_stocks,
#     })


@login_required
@user_passes_test(lambda u: u.role == 'RETAILER')
def retailer_dashboard(request):
    # Customer sales transactions (retailer as seller)
    customer_blocks = Block.objects.filter(chain_type='CUSTOMER').prefetch_related('transactions')
    customer_transactions = Transaction.objects.filter(
        retailer=request.user,
        chain_type='CUSTOMER'
    ).select_related('customer', 'product__product__product').prefetch_related(
        Prefetch('block_set', queryset=customer_blocks, to_attr='blocks')
    ).order_by('-timestamp')

    # Distributor purchase transactions (retailer as buyer)
    distributor_blocks = Block.objects.filter(chain_type='DISTRIBUTOR').prefetch_related('transactions')
    distributor_transactions = Transaction.objects.filter(
        customer=request.user,
        chain_type='DISTRIBUTOR'
    ).select_related('retailer', 'product__product__product').prefetch_related(
        Prefetch('block_set', queryset=distributor_blocks, to_attr='blocks')
    ).order_by('-timestamp')

    distributor_products = DistributorStock.objects.select_related('product', 'distributor').filter(available_quantity__gt=0)
    my_stocks = RetailerStock.objects.filter(retailer=request.user)

    return render(request, 'core/retailer_dashboard.html', {
        'customer_transactions': customer_transactions,
        'distributor_transactions': distributor_transactions,
        'distributor_products': distributor_products,
        'my_stocks': my_stocks,
    })


# @login_required
# @user_passes_test(lambda u: u.role == 'RETAILER')
# def retailer_dashboard(request):
#     # Fetch transactions for this retailer
#     transactions = Transaction.objects.filter(
#         retailer=request.user
#     ).select_related(
#         'customer', 'product__product__product'
#     ).prefetch_related('block_set').order_by('-timestamp')

#     distributor_products = DistributorStock.objects.select_related('product', 'distributor').filter(available_quantity__gt=0)
#     my_stocks = RetailerStock.objects.filter(retailer=request.user)

#     return render(request, 'core/retailer_dashboard.html', {
#         'transactions': transactions,  # Now passed to template
#         'distributor_products': distributor_products,
#         'my_stocks': my_stocks,
#     })



def register_retailer(request):
    if request.method == 'POST':
        form = RetailerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RetailerSignUpForm()
    return render(request, 'core/register_retailer.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'core/register_customer.html', {'form': CustomerSignUpForm()})




from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    role = request.GET.get('role', 'customer').upper()
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'role') and user.role.upper() == role:
                auth_login(request, user)
                # Redirect to dashboard based on role
                if role == 'MANUFACTURER':
                    return redirect('manufacturer_dashboard')
                elif role == 'DISTRIBUTOR':
                    return redirect('distributor_dashboard')
                elif role == 'RETAILER':
                    return redirect('retailer_dashboard')
                elif role == 'CUSTOMER':
                    return redirect('customer_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, f"Invalid credentials for {role.title()} login.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/login.html', {'form': form, 'role': role.title()})


from django.contrib.auth.decorators import login_required, user_passes_test  # 🔧 ADDED 'user_passes_test'


@login_required
@user_passes_test(lambda u: u.role == 'MANUFACTURER')
def add_product(request):
    if request.method == 'POST':
        form = ManufacturerProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.manufacturer = request.user
            product.save()
            return redirect('manufacturer_dashboard')
    else:
        form = ManufacturerProductForm()
    return render(request, 'core/add_product.html', {'form': form})








@login_required
@user_passes_test(lambda u: u.role == 'MANUFACTURER')
def edit_product(request, product_id):
    product = ManufacturerProduct.objects.get(id=product_id)
    
    # Verify ownership
    if product.manufacturer != request.user:
        messages.error(request, "You don't have permission to edit this product")
        return redirect('manufacturer_dashboard')

    if request.method == 'POST':
        form = ManufacturerProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('manufacturer_dashboard')
    else:
        form = ManufacturerProductForm(instance=product)

    return render(request, 'core/edit_product.html', {
        'form': form,
        'product': product
    })



@login_required
@user_passes_test(lambda u: u.role == 'MANUFACTURER')
def add_product(request):
    if request.method == 'POST':
        form = ManufacturerProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.manufacturer = request.user
            product.save()
            return redirect('manufacturer_dashboard')
    else:
        form = ManufacturerProductForm()
    return render(request, 'core/add_product.html', {'form': form})





# @login_required
# @user_passes_test(lambda u: u.role == 'MANUFACTURER')  # 🔧 ALREADY PRESENT
# def manufacturer_dashboard(request):
#     # products = ManufacturerProduct.objects.filter(manufacturer=request.user)
#     products = ManufacturerProduct.objects.filter(
#         manufacturer=request.user,
#         available_quantity__gt=0  # Added
#     )
#     return render(request, 'core/manufacturer_dashboard.html', {'products': products})

@login_required
@user_passes_test(lambda u: u.role == 'MANUFACTURER')
def manufacturer_dashboard(request):
    # Existing products query
    products = ManufacturerProduct.objects.filter(
        manufacturer=request.user,
        available_quantity__gt=0  # Show only available products
    )
    
    # New sales transactions (manufacturer as seller)
    sales_transactions = Transaction.objects.filter(
        retailer=request.user,  # Manufacturer is the seller
        chain_type='DISTRIBUTOR'
    ).select_related(
        'manu_product', 'customer'  # Customer is the distributor
    ).prefetch_related(
        Prefetch('block_set', queryset=Block.objects.prefetch_related('transactions'), to_attr='blocks')
    ).order_by('-timestamp')

    return render(request, 'core/manufacturer_dashboard.html', {
        'products': products,
        'sales_transactions': sales_transactions  # Add sales data to context
    })


@login_required
@user_passes_test(lambda u: u.role == 'MANUFACTURER')
def delete_product(request, product_id):
    try:
        product = ManufacturerProduct.objects.get(id=product_id)
        if product.manufacturer == request.user:
            product.delete()
            messages.success(request, "Product deleted successfully!")
        else:
            messages.error(request, "You don't have permission to delete this product")
    except ManufacturerProduct.DoesNotExist:
        messages.error(request, "Product not found")
    
    return redirect('manufacturer_dashboard')



# @login_required
# @user_passes_test(lambda u: u.role == 'MANUFACTURER')
# def register_distributor(request):
#     if request.method == 'POST':
#         form = DistributorSignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Distributor registered successfully!")
#             return redirect('manufacturer_dashboard')
#     else:
#         form = DistributorSignUpForm()
#     return render(request, 'core/register_distributor.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'MANUFACTURER')
def register_distributor(request):
    if request.method == 'POST':
        form = DistributorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Distributor registered successfully!")
            return redirect('manufacturer_dashboard')
    else:
        form = DistributorSignUpForm()
    return render(request, 'core/register_distributor.html', {'form': form})


# from django.contrib import messages
# from django.shortcuts import get_object_or_404


# @login_required
# @user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
# def add_to_distributor_stock(request, product_id):
#     manufacturer_product = get_object_or_404(ManufacturerProduct, id=product_id)
    
#     if request.method == 'POST':
#         # 🔧 VALIDATE INPUTS BEFORE CONVERSION
#         quantity_str = request.POST.get('quantity')
#         price_str = request.POST.get('price')
        
#         if not quantity_str or not price_str:
#             messages.error(request, "Please fill in all fields")
#             return redirect('distributor_dashboard')
        
#         try:
#             quantity = int(quantity_str)
#             price = float(price_str)
#         except ValueError:
#             messages.error(request, "Invalid input values")
#             return redirect('distributor_dashboard')
        
#         # 🔧 ADD QUANTITY VALIDATION
#         if quantity <= 0 or quantity > manufacturer_product.available_quantity:
#             messages.error(request, "Invalid quantity")
#             return redirect('distributor_dashboard')
        
#         # 🔧 ADD PRICE VALIDATION
#         if price <= 0:
#             messages.error(request, "Price must be greater than 0")
#             return redirect('distributor_dashboard')
        
#         # 🔧 CREATE DISTRIBUTOR STOCK
#         try:
#             DistributorStock.objects.create(
#                 distributor=request.user,
#                 product=manufacturer_product,
#                 price=price,
#                 available_quantity=quantity
#             )
            
#             # 🔧 UPDATE MANUFACTURER'S STOCK
#             manufacturer_product.available_quantity -= quantity
#             manufacturer_product.save()
            
#             messages.success(request, "Stock added successfully!")
#         except Exception as e:
#             messages.error(request, "Failed to add stock: " + str(e))
        
#         return redirect('distributor_dashboard')
    
#     return redirect('distributor_dashboard')



from django.contrib import messages
from django.shortcuts import get_object_or_404
@login_required
@user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
def add_to_distributor_stock(request, product_id):
    manufacturer_product = get_object_or_404(ManufacturerProduct, id=product_id)

    if request.method == 'POST':
        quantity_str = request.POST.get('quantity')
        price_str = request.POST.get('price')
        if not quantity_str or not price_str:
            messages.error(request, "Please fill in all fields")
            return redirect('distributor_dashboard')
        try:
            quantity = int(quantity_str)
            price = float(price_str)
        except ValueError:
            messages.error(request, "Invalid input values")
            return redirect('distributor_dashboard')
        if quantity <= 0 or quantity > manufacturer_product.available_quantity:
            messages.error(request, "Invalid quantity")
            return redirect('distributor_dashboard')
        if price <= 0:
            messages.error(request, "Price must be greater than 0")
            return redirect('distributor_dashboard')

        # Store inputs in session
        request.session['temp_distributor_data'] = {
            'product_id': product_id,
            'quantity': quantity,
            'price': price
        }
        return redirect('confirm_distributor_stock', product_id=product_id)

    return redirect('distributor_dashboard')
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction
from .models import ManufacturerProduct, DistributorStock, Transaction
from .blockchain import Blockchain

@login_required
@user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
def confirm_distributor_stock(request, product_id):
    manufacturer_product = get_object_or_404(ManufacturerProduct, id=product_id)
    temp_data = request.session.get('temp_distributor_data')
    
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', '').strip()
        
        # Check for duplicate transaction ID
        if Transaction.objects.filter(transaction_id=transaction_id).exists():
            messages.error(request, "This Transaction ID already exists")
            return redirect('confirm_distributor_stock', product_id=product_id)
        
        # Create transaction with atomic operation
        with transaction.atomic():
            try:
                # Create Distributor Stock
                distributor_stock = DistributorStock.objects.create(
                    distributor=request.user,
                    product=manufacturer_product,
                    price=temp_data['price'],
                    available_quantity=temp_data['quantity'],
                    transaction_id=transaction_id
                )

                # Create Transaction
                tx = Transaction.objects.create(
                    transaction_id=transaction_id,
                    manu_product=manufacturer_product,  # Use correct field
                    quantity=temp_data['quantity'],
                    amount=manufacturer_product.base_price * temp_data['quantity'],
                    customer=request.user,  # Distributor as buyer
                    retailer=manufacturer_product.manufacturer,  # Manufacturer as seller
                    chain_type='DISTRIBUTOR',
                    timestamp=timezone.now()
                )

                # Add to DISTRIBUTOR blockchain
                distributor_blockchain = Blockchain(chain_type='DISTRIBUTOR')
                distributor_blockchain.current_transactions.append(tx)
                last_proof = distributor_blockchain.last_block.proof if distributor_blockchain.last_block else 0
                proof = distributor_blockchain.proof_of_work(last_proof)
                distributor_blockchain.new_block(proof)

                # Update Manufacturer Stock
                manufacturer_product.available_quantity -= temp_data['quantity']
                manufacturer_product.save()
                
                del request.session['temp_distributor_data']
                messages.success(request, "Stock added successfully!")
                return redirect('distributor_dashboard')
            except Exception as e:
                messages.error(request, f"Transaction failed: {str(e)}")
                return redirect('confirm_distributor_stock', product_id=product_id)
    return render(request, 'core/confirm_distributor_stock.html', {
        'manufacturer_product': manufacturer_product,
        'temp_data': temp_data
    })





@login_required
@user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
def edit_distributor_stock(request, stock_id):
    stock = get_object_or_404(DistributorStock, id=stock_id)

    if stock.distributor != request.user:
        messages.error(request, "You don't have permission to edit this stock")
        return redirect('distributor_dashboard')

    if request.method == 'POST':
        form = DistributorStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Price updated successfully!")
            return redirect('distributor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DistributorStockForm(instance=stock)

    return render(request, 'core/edit_distributor_stock.html', {
        'form': form,
        'stock': stock,
    })


@login_required
@user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
def add_more_stock(request, stock_id):
    stock = get_object_or_404(DistributorStock, id=stock_id)
    if stock.distributor != request.user:
        messages.error(request, "You don't have permission to modify this stock")
        return redirect('distributor_dashboard')
    
    manufacturer_product = stock.product
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        
        if quantity <= 0 or quantity > manufacturer_product.available_quantity:
            messages.error(request, "Invalid quantity")
            return redirect('distributor_dashboard')
        
        try:
            # Update distributor's stock
            stock.available_quantity += quantity
            stock.save()
            
            # Update manufacturer's stock
            manufacturer_product.available_quantity -= quantity
            manufacturer_product.save()
            
            messages.success(request, f"Added {quantity} more units to {{ stock.product.name }}")
        except Exception as e:
            messages.error(request, "Failed to add stock: " + str(e))
        
        return redirect('distributor_dashboard')
    
    return render(request, 'core/add_more_stock.html', {
        'stock': stock,
        'max_quantity': stock.product.available_quantity,
    })



from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.role == 'RETAILER')
def retailer_add_product(request):
    if request.method == 'POST':
        form = RetailerStockForm(request.POST, request.FILES)  # You need to create this form
        if form.is_valid():
            retailer_stock = form.save(commit=False)
            retailer_stock.retailer = request.user
            retailer_stock.save()
            messages.success(request, 'Product added successfully.')
            return redirect('retailer_dashboard')
    else:
        form = RetailerStockForm()
    return render(request, 'core/retailer_add_product.html', {'form': form})


# @login_required
# @user_passes_test(lambda u: u.role == 'RETAILER')
# def retailer_dashboard(request):
#     # Products available from all distributors
#     distributor_products = DistributorStock.objects.select_related('product', 'distributor').filter(available_quantity__gt=0)
#     # Products this retailer has already added for customers
#     my_stocks = RetailerStock.objects.filter(retailer=request.user)
#     return render(request, 'core/retailer_dashboard.html', {
#         'distributor_products': distributor_products,
#         'my_stocks': my_stocks,
#     })

# @login_required
# @user_passes_test(lambda u: u.role == 'RETAILER')
# def add_to_retailer_stock(request, stock_id):
#     distributor_stock = get_object_or_404(DistributorStock, id=stock_id)
#     if request.method == 'POST':
#         quantity_str = request.POST.get('quantity')
#         price_str = request.POST.get('price')
#         if not quantity_str or not price_str:
#             messages.error(request, "Please fill in all fields")
#             return redirect('retailer_dashboard')
#         try:
#             quantity = int(quantity_str)
#             price = float(price_str)
#         except ValueError:
#             messages.error(request, "Invalid input values")
#             return redirect('retailer_dashboard')
#         if quantity <= 0 or quantity > distributor_stock.available_quantity:
#             messages.error(request, "Invalid quantity")
#             return redirect('retailer_dashboard')
#         if price <= 0:
#             messages.error(request, "Price must be greater than 0")
#             return redirect('retailer_dashboard')
#         # Create retailer stock
#         RetailerStock.objects.create(
#             retailer=request.user,
#             product=distributor_stock,
#             price=price,
#             available_quantity=quantity
#         )
#         # Update distributor's available quantity
#         distributor_stock.available_quantity -= quantity
#         distributor_stock.save()
#         messages.success(request, "Product added to your stock!")
#         return redirect('retailer_dashboard')
#     return redirect('retailer_dashboard')

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import DistributorStock, RetailerStock

@login_required
@user_passes_test(lambda u: u.role == 'RETAILER')
def add_to_retailer_stock(request, stock_id):
    distributor_stock = get_object_or_404(DistributorStock, id=stock_id)
    
    if request.method == 'POST':
        # Store temporary data in session
        request.session['temp_stock_data'] = {
            'stock_id': stock_id,
            'quantity': int(request.POST.get('quantity')),
            'price': float(request.POST.get('price'))
        }
        return redirect('confirm_retailer_stock', stock_id=stock_id)
        
    return redirect('retailer_dashboard')

# @login_required
# @user_passes_test(lambda u: u.role == 'RETAILER')
# def confirm_retailer_stock(request, stock_id):
#     distributor_stock = get_object_or_404(DistributorStock, id=stock_id)
    
#     if request.method == 'POST':
#         transaction_id = request.POST.get('transaction_id', '').strip()
#         if not transaction_id:
#             messages.error(request, "Transaction ID is required")
#             return redirect('confirm_retailer_stock', stock_id=stock_id)
            
#         temp_data = request.session.get('temp_stock_data')
#         if not temp_data or temp_data['stock_id'] != stock_id:
#             messages.error(request, "Session expired. Please start over.")
#             return redirect('retailer_dashboard')
            
#         try:
#             # Create RetailerStock
#             retailer_stock = RetailerStock.objects.create(
#                 retailer=request.user,
#                 product=distributor_stock,
#                 price=temp_data['price'],
#                 available_quantity=temp_data['quantity'],
#                 transaction_id=transaction_id
#             )
            
#             # Create blockchain transaction
#             tx = Transaction.objects.create(
#                 transaction_id=transaction_id,
#                 product=retailer_stock,
#                 quantity=temp_data['quantity'],
#                 amount=distributor_stock.price * temp_data['quantity'],
#                 customer=request.user,  # Retailer as buyer
#                 retailer=distributor_stock.distributor,  # Distributor as seller [3][7]
#                 timestamp=timezone.now()
#             )

#             # Add to blockchain
#             blockchain = Blockchain()
#             blockchain.current_transactions.append(tx)
            
#             last_proof = blockchain.last_block.proof if blockchain.last_block else 0
#             proof = blockchain.proof_of_work(last_proof)
#             previous_hash = blockchain.hash(blockchain.last_block) if blockchain.last_block else '1'
            
#             block = blockchain.new_block(proof, previous_hash)
#             block.transactions.add(tx)

#             # Update distributor stock
#             distributor_stock.available_quantity -= temp_data['quantity']
#             distributor_stock.save()
            
#             del request.session['temp_stock_data']
#             messages.success(request, "Stock added and blockchain updated!")
#             return redirect('retailer_dashboard')
            
#         except Exception as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('confirm_retailer_stock', stock_id=stock_id)
    
#     return render(request, 'core/confirm_retailer_stock.html', {
#         'distributor_stock': distributor_stock,
#         'distributor_price': distributor_stock.price  # Pass to template
#     })
@login_required
@user_passes_test(lambda u: u.role == 'RETAILER')
def confirm_retailer_stock(request, stock_id):
    distributor_stock = get_object_or_404(DistributorStock, id=stock_id)
    
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', '').strip()
        if not transaction_id:
            messages.error(request, "Transaction ID is required")
            return redirect('confirm_retailer_stock', stock_id=stock_id)
            
        temp_data = request.session.get('temp_stock_data')
        if not temp_data or temp_data['stock_id'] != stock_id:
            messages.error(request, "Session expired. Please start over.")
            return redirect('retailer_dashboard')
            
        try:
            # Create RetailerStock
            retailer_stock = RetailerStock.objects.create(
                retailer=request.user,
                product=distributor_stock,
                price=temp_data['price'],
                available_quantity=temp_data['quantity'],
                transaction_id=transaction_id
            )
            
            # Create DISTRIBUTOR-CHAIN transaction
            tx = Transaction.objects.create(
                transaction_id=transaction_id,
                product=retailer_stock,
                quantity=temp_data['quantity'],
                amount=distributor_stock.price * temp_data['quantity'],
                customer=request.user,  # Retailer as buyer
                retailer=distributor_stock.distributor,  # Actual distributor
                chain_type='DISTRIBUTOR',  # Critical chain type specification
                timestamp=timezone.now()
            )

            # Add to DISTRIBUTOR blockchain
            distributor_blockchain = Blockchain(chain_type='DISTRIBUTOR')
            distributor_blockchain.current_transactions.append(tx)
            
            # Get last proof from distributor chain
            last_proof = distributor_blockchain.last_block.proof if distributor_blockchain.last_block else 0
            proof = distributor_blockchain.proof_of_work(last_proof)
            
            # Create new block in distributor chain
            block = distributor_blockchain.new_block(proof)
            block.transactions.add(tx)

            # Update distributor stock
            distributor_stock.available_quantity -= temp_data['quantity']
            distributor_stock.save()
            
            del request.session['temp_stock_data']
            messages.success(request, "Stock added to distributor blockchain!")
            return redirect('retailer_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('confirm_retailer_stock', stock_id=stock_id)
    
    return render(request, 'core/confirm_retailer_stock.html', {
        'distributor_stock': distributor_stock,
        'distributor_price': distributor_stock.price
    })


from django.db import transaction
from .models import Transaction, Block, RetailerStock, Order
from .blockchain import Blockchain

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import RetailerStock, Order, Transaction, Block
from .blockchain import Blockchain

from django.utils import timezone

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import RetailerStock, Order, Transaction, Block
from .blockchain import Blockchain

@login_required
@user_passes_test(lambda u: u.role == 'CUSTOMER')
@transaction.atomic
def buy_product(request, product_id):
    retailer_stock = get_object_or_404(RetailerStock, id=product_id)
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', '').strip()
        quantity_str = request.POST.get('quantity', '')
        
        # Validate inputs
        if not transaction_id:
            messages.error(request, "Transaction ID is required.")
            return redirect('buy_product', product_id=product_id)
            
        try:
            quantity = int(quantity_str)
            if quantity < 1 or quantity > retailer_stock.available_quantity:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity specified.")
            return redirect('buy_product', product_id=product_id)

        # Check transaction ID uniqueness
        if Transaction.objects.filter(transaction_id=transaction_id).exists():
            messages.error(request, "This transaction ID already exists.")
            return redirect('buy_product', product_id=product_id)

        try:
            # Reduce stock
            retailer_stock.available_quantity -= quantity
            retailer_stock.save()

            # Create order
            Order.objects.create(
                customer=request.user,
                product=retailer_stock,
                quantity=quantity
            )

            # Create transaction
            tx = Transaction.objects.create(
                transaction_id=transaction_id,
                product=retailer_stock,
                quantity=quantity,
                amount=retailer_stock.price * quantity,
                customer=request.user,
                retailer=retailer_stock.retailer,
                timestamp=timezone.now()
            )

            # Add to blockchain
            blockchain = Blockchain()
            # Get the last proof
            last_proof = blockchain.last_block.proof if blockchain.last_block else 0
            # Calculate new proof
            proof = blockchain.proof_of_work(last_proof)
            
            # Create new block
            previous_hash = blockchain.hash(blockchain.last_block) if blockchain.last_block else '1'
            block = Block.objects.create(
            index=len(blockchain.chain) + 1,
            proof=proof,
            previous_hash=previous_hash,
            timestamp=timezone.now()
        )
            block.transactions.add(tx)
            blockchain.chain.append(block)
            messages.success(request, "Purchase successful! Transaction added to blockchain.")
            return redirect('customer_dashboard')
            
        except Exception as e:
            # Rollback on error
            messages.error(request, f"Transaction failed: {str(e)}")
            return redirect('buy_product', product_id=product_id)
            
    return render(request, 'core/buy_product.html', {'retailer_stock': retailer_stock})




# @login_required
# @user_passes_test(lambda u: u.role == 'CUSTOMER')
# @transaction.atomic
# def buy_product(request, product_id):
#     retailer_stock = get_object_or_404(RetailerStock, id=product_id)
#     if request.method == 'POST':
#         transaction_id = request.POST.get('transaction_id', '').strip()
#         quantity_str = request.POST.get('quantity', '')
        
#         # Validate inputs
#         if not transaction_id:
#             messages.error(request, "Transaction ID is required.")
#             return redirect('buy_product', product_id=product_id)
            
#         try:
#             quantity = int(quantity_str)
#             if quantity < 1 or quantity > retailer_stock.available_quantity:
#                 raise ValueError
#         except (ValueError, TypeError):
#             messages.error(request, "Invalid quantity specified.")
#             return redirect('buy_product', product_id=product_id)

#         # Check transaction ID uniqueness
#         if Transaction.objects.filter(transaction_id=transaction_id).exists():
#             messages.error(request, "This transaction ID already exists.")
#             return redirect('buy_product', product_id=product_id)

#         try:
#             # Reduce stock and create records
#             retailer_stock.available_quantity -= quantity
#             retailer_stock.save()

#             Order.objects.create(
#                 customer=request.user,
#                 product=retailer_stock,
#                 quantity=quantity
#             )

#             tx = Transaction.objects.create(
#                 transaction_id=transaction_id,
#                 product=retailer_stock,
#                 quantity=quantity,
#                 amount=retailer_stock.price * quantity,
#                 customer=request.user,
#                 retailer=retailer_stock.retailer,  # Critical retailer link
#                 timestamp=timezone.now()
#             )

#             # Blockchain integration
#             blockchain = Blockchain()
#             blockchain.current_transactions.append(tx)  # Add to pending transactions
#             last_block = blockchain.last_block
            
#             proof = blockchain.proof_of_work(last_block.proof if last_block else 0)
#             previous_hash = blockchain.hash(last_block) if last_block else '1'
            
#             # Create and save block
#             block = blockchain.new_block(proof, previous_hash)
#             block.transactions.add(tx)  # Explicit M2M relationship
            
#             messages.success(request, "Purchase successful! Transaction added to blockchain.")
#             return redirect('customer_dashboard')
            
#         except Exception as e:
#             messages.error(request, f"Transaction failed: {str(e)}")
#             return redirect('buy_product', product_id=product_id)
            
#     return render(request, 'core/buy_product.html', {'retailer_stock': retailer_stock})





@login_required
@user_passes_test(lambda u: u.role == 'RETAILER')
def confirm_retailer_stock(request, stock_id):
    distributor_stock = get_object_or_404(DistributorStock, id=stock_id)
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', '').strip()
        if not transaction_id:
            messages.error(request, "Transaction ID is required")
            return redirect('confirm_retailer_stock', stock_id=stock_id)

        temp_data = request.session.get('temp_stock_data')
        if not temp_data or temp_data['stock_id'] != stock_id:
            messages.error(request, "Session expired. Please start over.")
            return redirect('retailer_dashboard')

        try:
            retailer_stock = RetailerStock.objects.create(
                retailer=request.user,
                product=distributor_stock,
                price=temp_data['price'],
                available_quantity=temp_data['quantity'],
                transaction_id=transaction_id
            )

            tx = Transaction.objects.create(
                transaction_id=transaction_id,
                product=retailer_stock,
                quantity=temp_data['quantity'],
                amount=distributor_stock.price * temp_data['quantity'],
                customer=request.user,  # Retailer as buyer
                retailer=distributor_stock.distributor,  # Distributor as seller
                chain_type='DISTRIBUTOR',
                timestamp=timezone.now()
            )

            distributor_blockchain = Blockchain(chain_type='DISTRIBUTOR')
            distributor_blockchain.current_transactions.append(tx)
            last_proof = distributor_blockchain.last_block.proof if distributor_blockchain.last_block else 0
            proof = distributor_blockchain.proof_of_work(last_proof)
            distributor_blockchain.new_block(proof)

            distributor_stock.available_quantity -= temp_data['quantity']
            distributor_stock.save()

            del request.session['temp_stock_data']
            messages.success(request, "Stock added and blockchain updated!")
            return redirect('retailer_dashboard')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('confirm_retailer_stock', stock_id=stock_id)

    return render(request, 'core/confirm_retailer_stock.html', {
        'distributor_stock': distributor_stock,
        'distributor_price': distributor_stock.price
    })
















# @login_required
# @user_passes_test(lambda u: u.role == 'DISTRIBUTOR')
# def confirm_distributor_stock(request, stock_id):
#     manufacturer_product = get_object_or_404(ManufacturerProduct, id=stock_id)
    
#     if request.method == 'POST':
#         transaction_id = request.POST.get('transaction_id', '').strip()
#         if not transaction_id:
#             messages.error(request, "Transaction ID is required")
#             return redirect('confirm_distributor_stock', stock_id=stock_id)
            
#         # Retrieve temporary data from session
#         temp_data = request.session.get('temp_distributor_data')
#         if not temp_data or temp_data['stock_id'] != stock_id:
#             messages.error(request, "Session expired. Please start over.")
#             return redirect('distributor_dashboard')
            
#         try:
#             # Check for existing transaction ID
#             if DistributorStock.objects.filter(transaction_id=transaction_id).exists():
#                 messages.error(request, "This Transaction ID already exists")
#                 return redirect('confirm_distributor_stock', stock_id=stock_id)
            
#             # Create DistributorStock
#             distributor_stock = DistributorStock.objects.create(
#                 distributor=request.user,
#                 product=manufacturer_product,
#                 price=temp_data['price'],
#                 available_quantity=temp_data['quantity'],
#                 transaction_id=transaction_id
#             )
            
#             # Create Transaction
#             tx = Transaction.objects.create(
#                 transaction_id=transaction_id,
#                 product=distributor_stock,
#                 quantity=temp_data['quantity'],
#                 amount=manufacturer_product.base_price * temp_data['quantity'],
#                 customer=request.user,  # Distributor as buyer
#                 retailer=manufacturer_product.manufacturer,  # Manufacturer as seller
#                 chain_type='DISTRIBUTOR',
#                 timestamp=timezone.now()
#             )
            
#             # Add to blockchain
#             blockchain = Blockchain(chain_type='DISTRIBUTOR')
#             blockchain.current_transactions.append(tx)
#             last_proof = blockchain.last_block.proof if blockchain.last_block else 0
#             proof = blockchain.proof_of_work(last_proof)
#             blockchain.new_block(proof)
            
#             # Update manufacturer stock
#             manufacturer_product.available_quantity -= temp_data['quantity']
#             manufacturer_product.save()
            
#             # Clear session data
#             del request.session['temp_distributor_data']
            
#             messages.success(request, "Stock added successfully!")
#             return redirect('distributor_dashboard')
            
#         except Exception as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('confirm_distributor_stock', stock_id=stock_id)
    
#     return render(request, 'core/confirm_distributor_stock.html', {
#         'manufacturer_product': manufacturer_product
#     })
