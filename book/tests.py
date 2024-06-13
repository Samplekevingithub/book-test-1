from django.test import TestCase

# Create your tests here.

# {% extends 'book/basic.html' %}
# {% block checkoutactive %} active {% endblock checkoutactive %}
# {% block css %}
#     body {
#         font-family: Arial, sans-serif;
#     }
#     .container {
#         max-width: 500px;
#         margin: 0 auto;
#         padding: 20px;
#         border: 1px solid #ccc;
#         border-radius: 5px;
#         box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#     }
#     .form-group {
#         margin-bottom: 20px;
#     }
#     label {
#         font-weight: bold;
#     }
#     input[type="date"] {
#         width: 100%;
#         padding: 10px;
#         border: 1px solid #ccc;
#         border-radius: 5px;
#     }
#     button[type="submit"] {
#         background-color: #007bff;
#         color: #fff;
#         border: none;
#         padding: 10px 20px;
#         border-radius: 5px;
#         cursor: pointer;
#         transition: background-color 0.3s;
#     }
#     button[type="submit"]:hover {
#         background-color: #0056b3;
#     }
#     {% endblock %}
# {% block body %}
# <div class="container my-3">
#     <h2>Rented Books</h2>
#     {% if rented_books %}
#         <ul>
#             {% for rental in rented_books %}
#                 <li>
#                     <strong>{{ rental.book.title }}</strong>
#                     <ul>
#                         <li>Rental Date: {{ rental.rental_date }}</li>
#                         <li>Return Date: {{ rental.return_date }}</li>
#                         <li>Fee: ${{ rental.fee }}</li>
#                     </ul>
#                 </li>
#             {% endfor %}
#         </ul>
#         <p>Total Bill: ${{ total_bill }}</p>
#     {% else %}
#         <p>No books rented.</p>
#     {% endif %}
# </div>
# {% endblock %} 

