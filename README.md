# solana-account-vis
Use Seaborn to visually interpret the byte layout of Solana account types

# Usage
```
from account_visualization import generate_account_visualization

token_account = OrderedDict(
    mint=('Pubkey', 32),
    owner=('Pubkey', 32),
    amount=('u64', 8),
    delegate=('COption<Pubkey>', 36),
    state=('AccountState', 1),
    is_native=('COption<u64>', 12),
    delegated_amount=('u64', 8),
    close_authority=('COption<Pubkey>', 36),
)

mint = OrderedDict(
    mint_authority=('Pubkey', 32),
    supply=('u64', 8),
    decimals=('u8', 1),
    is_initialized=(bool, 1),
    freeze_authority=('COption<Pubkey>', 36),
)

generate_account_visualization(token_account, title="Token Account Layout")
generate_account_visualization(mint, title="Mint Layout")
```

# Output
