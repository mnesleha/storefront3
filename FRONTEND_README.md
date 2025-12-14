# Storefront Frontend

Modern, responsive frontend for the Storefront e-commerce Django application.

## Features

- **Product Catalog**: Browse products with filtering, search, and sorting
- **Shopping Cart**: Add/remove items, update quantities
- **User Authentication**: Login, registration, and profile management
- **Order Management**: View order history and details
- **Responsive Design**: Mobile-friendly layout using modern CSS3
- **REST API Integration**: Seamless integration with Django REST Framework backend

## Pages

### Public Pages

- **Home** (`/`) - Landing page with featured products
- **Products** (`/store/products/`) - Product listing with filters
- **Product Detail** (`/store/products/<id>/`) - Individual product details
- **Collections** (`/store/collections/`) - Browse product collections
- **Login** (`/login/`) - User login
- **Register** (`/register/`) - New user registration

### Protected Pages

- **Profile** (`/profile/`) - User profile management
- **Cart** (`/store/cart/`) - Shopping cart
- **Checkout** (`/store/checkout/`) - Order checkout
- **My Orders** (`/store/orders/`) - Order history

## Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables and Grid/Flexbox
- **JavaScript (Vanilla)** - Client-side functionality
- **Django Template Language** - Server-side templating

## Setup for Development

1. Collect static files:

```bash
python manage.py collectstatic --noinput
```

2. Run the development server:

```bash
python manage.py runserver
```

3. Access the frontend at `http://localhost:8000`

## Deployment on Heroku

The application is configured for Heroku deployment:

1. **Procfile** includes static file collection
2. **WhiteNoise** serves static files in production
3. **Gunicorn** WSGI server for production

Static files are automatically collected during deployment via the `release` command in Procfile.

## Frontend Architecture

### Template Structure

```
templates/
├── base.html                 # Base template with navbar and footer
├── core/
│   ├── home.html            # Landing page
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   └── profile.html         # User profile
└── store/
    ├── product_list.html    # Product catalog
    ├── product_detail.html  # Product details
    ├── collection_list.html # Collections
    ├── cart.html            # Shopping cart
    ├── checkout.html        # Checkout
    └── order_list.html      # Order history
```

### Static Files

```
static/
├── css/
│   └── main.css             # Main stylesheet
├── js/
│   └── main.js              # JavaScript functionality
└── images/
    └── no-image.png         # Placeholder image
```

## API Integration

The frontend uses the Django REST Framework API for:

- Product data
- Cart management
- Order creation
- User authentication (JWT)

### Authentication Flow

1. User logs in via `/login/`
2. JWT tokens stored in localStorage
3. API requests include JWT token in Authorization header
4. Protected pages check for valid token

## Customization

### Styling

Edit `static/css/main.css` to customize:

- Color scheme (CSS variables at top of file)
- Layout and spacing
- Component styles

### Templates

Modify templates in `templates/` directory:

- Extend `base.html` for consistent layout
- Use Django template tags for dynamic content
- Add custom blocks for page-specific content

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Enhancements

- Product image gallery
- Review ratings with stars
- Wishlist functionality
- Advanced filtering
- Order tracking
- Payment integration
- Social authentication
