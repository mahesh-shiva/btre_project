from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contacts


def contact(request):
    if request.method == "POST":
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        listing_id = request.POST['listing_id']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made enquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contacts.objects.filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an enquiry for this listing!')
                return redirect('/listings/' + listing_id)

        contact_inquiry = Contacts(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone,
                                   message=message, user_id=user_id)

        contact_inquiry.save()

        # Send email to realtor
        send_mail(
            'Property listing enquiry',
            'There has been an inquiry for ' + listing + '. Sign in to admin portal for more info',
            'shiva.mahesh59@gmail.com',
            [realtor_email, 'mahesh@ridecell.com'],
            fail_silently=False
        )

        messages.success(request, "Your request has been successfully submitted. A realtor will get back to you soon!")
        return redirect('/listings/' + listing_id)

