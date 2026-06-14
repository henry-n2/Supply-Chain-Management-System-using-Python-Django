# from .models import Block, Transaction
# import hashlib
# from django.utils import timezone

# class Blockchain:
#     def __init__(self):
#         self.chain = list(Block.objects.all().order_by('index'))
#         self.current_transactions = []

#     def proof_of_work(self, last_proof):
#         proof = 0
#         while not self.valid_proof(last_proof, proof):
#             proof += 1
#         return proof

#     def valid_chain(self):
#         """Verify the blockchain's integrity"""
#         if not self.chain:
#             return True

#         previous_block = self.chain[0]
#         current_index = 1

#         while current_index < len(self.chain):
#             block = self.chain[current_index]
            
#             # Check previous hash
#             if block.previous_hash != self.hash(previous_block):
#                 return False

#             # Check proof validity
#             if not self.valid_proof(previous_block.proof, block.proof):
#                 return False

#             previous_block = block
#             current_index += 1

#         return True

#     @staticmethod
#     def valid_proof(last_proof, proof):
#         """Validate the proof-of-work"""
#         guess = f'{last_proof}{proof}'.encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()
#         return guess_hash.startswith('0000')  # Adjust difficulty as needed
    
#     @staticmethod
#     def hash(block):
#         block_string = f"{block.index}{block.timestamp}{block.proof}{block.previous_hash}".encode()
#         return hashlib.sha256(block_string).hexdigest()

#     @property
#     def last_block(self):
#         return self.chain[-1] if self.chain else None


# def new_block(self, proof):
#         previous_hash = self.hash(self.last_block) if self.last_block else '1'
        
#         block = Block.objects.create(
#             index=len(self.chain) + 1,
#             proof=proof,
#             previous_hash=previous_hash,
#             timestamp=timezone.now()
#         )
#         block.transactions.set(self.current_transactions)
#         self.current_transactions = []
#         self.chain.append(block)
#         return block

# @staticmethod
# def hash(block):
#         block_string = f"{block.index}{block.timestamp}{block.proof}{block.previous_hash}".encode()
#         return hashlib.sha256(block_string).hexdigest()




from .models import Block, Transaction
import hashlib
from django.utils import timezone

# class Blockchain:
#     def __init__(self, chain_type='CUSTOMER'):
#         self.chain_type = chain_type
#         self.chain = list(Block.objects.filter(chain_type=chain_type).order_by('index'))
#         self.current_transactions = []

#     def proof_of_work(self, last_proof):
#         proof = 0
#         while not self.valid_proof(last_proof, proof):
#             proof += 1
#         return proof

#     def valid_chain(self):
#         """Verify the blockchain's integrity"""
#         if not self.chain:
#             return True

#         previous_block = self.chain[0]
#         current_index = 1

#         while current_index < len(self.chain):
#             block = self.chain[current_index]
            
#             if block.previous_hash != self.hash(previous_block):
#                 return False

#             if not self.valid_proof(previous_block.proof, block.proof):
#                 return False

#             previous_block = block
#             current_index += 1

#         return True

#     @staticmethod
#     def valid_proof(last_proof, proof):
#         guess = f'{last_proof}{proof}'.encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()
#         return guess_hash.startswith('0000')
# blockchain.py
# class Blockchain:
#     def __init__(self, chain_type='DISTRIBUTOR'):
#         self.chain_type = chain_type
#         self.chain = list(Block.objects.filter(chain_type=chain_type).order_by('index'))
#         self.current_transactions = []

#     def new_block(self, proof):
#         last_block = self.chain[-1] if self.chain else None
#         previous_hash = self.hash(last_block) if last_block else '1'
        
#         block = Block.objects.create(
#             index=len(self.chain) + 1,
#             proof=proof,
#             previous_hash=previous_hash,
#             chain_type=self.chain_type,
#             timestamp=timezone.now()
#         )
        
#         # Add transactions to block
#         block.transactions.set(self.current_transactions)
#         self.current_transactions = []
#         self.chain.append(block)
#         return block

#     def valid_chain(self):
#         if not self.chain:
#             return True
            
#         previous_block = self.chain[0]
#         current_index = 1
        
#         while current_index < len(self.chain):
#             block = self.chain[current_index]
#             if block.previous_hash != self.hash(previous_block):
#                 return False
#             if not self.valid_proof(previous_block.proof, block.proof):
#                 return False
#             previous_block = block
#             current_index += 1
#         return True

#     @staticmethod
#     def valid_proof(last_proof, proof):
#         guess = f'{last_proof}{proof}'.encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()
#         return guess_hash.startswith('0000')

#     def hash(self, block):
#         block_string = f"{self.chain_type}{block.index}{block.timestamp}{block.proof}".encode()
#         return hashlib.sha256(block_string).hexdigest()

#     @property
#     def last_block(self):
#         return self.chain[-1] if self.chain else None

#     def new_block(self, proof):
#         last_block_same_chain = Block.objects.filter(chain_type=self.chain_type).order_by('-index').first()
#         previous_hash = self.hash(last_block_same_chain) if last_block_same_chain else '1'
        
#         block = Block.objects.create(
#             index=Block.objects.filter(chain_type=self.chain_type).count() + 1,
#             proof=proof,
#             previous_hash=previous_hash,
#             chain_type=self.chain_type,
#             timestamp=timezone.now()
#         )
#         block.transactions.set(self.current_transactions)
#         self.current_transactions = []
#         self.chain.append(block)
#         return block



from .models import Block, Transaction
import hashlib
from django.utils import timezone

class Blockchain:
    def __init__(self, chain_type='DISTRIBUTOR'):
        self.chain_type = chain_type
        self.chain = list(Block.objects.filter(chain_type=chain_type).order_by('index'))
        self.current_transactions = []

    def proof_of_work(self, last_proof):
        """Find a number p' such that hash(pp') has 4 leading zeroes"""
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """Check if hash(last_proof, proof) starts with 4 zeroes"""
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith('0000')

    def new_block(self, proof):
        last_block = self.chain[-1] if self.chain else None
        previous_hash = self.hash(last_block) if last_block else '1'
        
        block = Block.objects.create(
            index=len(self.chain) + 1,
            proof=proof,
            previous_hash=previous_hash,
            chain_type=self.chain_type,
            timestamp=timezone.now()
        )
        block.transactions.set(self.current_transactions)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        """Creates SHA-256 hash of a Block"""
        block_string = f"{self.chain_type}{block.index}{block.timestamp}{block.proof}".encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    def valid_chain(self):
        """Verify the blockchain's integrity"""
        if not self.chain:
            return True
        previous_block = self.chain[0]
        current_index = 1
        while current_index < len(self.chain):
            block = self.chain[current_index]
            if block.previous_hash != self.hash(previous_block):
                return False
            if not self.valid_proof(previous_block.proof, block.proof):
                return False
            previous_block = block
            current_index += 1
        return True
