from django.urls import path
from .import views 
from .views import DynamicProductCreateView
urlpatterns = [
    path('admin-panel/dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/placed-oder-list/', views.show_placed_oder_list, name='show_placed_oder_list'),
    path('admin-panel/completed-oder-list/', views.show_completed_oder_list, name='show_completed_oder_list'),
    path('admin-panel/placed-oder-item-list/<int:id>', views.show_placed_oder_item_list, name='show_placed_oder_item_list'),
    path('admin-panel/completed-oder-item-list/<int:id>', views.show_completed_oder_item_list, name='show_completed_oder_item_list'),
    
     path('product-list/', views.product_list, name='product_list'),
    path('add-product/', views.create_product, name='add_product'),
    path('view-products/', views.view_products, name='view_products'),
        path('view-product-type/', views.create_product_type, name='product_type'),
   # path('add-category/', views.add_category, name='add_category'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('add-product-type/', views.add_product_type, name='add_product_type'),
     path('add-category/', views.add_category, name='add_category'),
      path('category-list/', views.category_list, name='category_list'),  # Ensure this exists
    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('manage_attributes/', views.manage_attributes, name='manage_attributes'),
    path('manage_attribute_values/<int:attribute_id>/', views.manage_attribute_values, name='manage_attribute_values'),
    
]
