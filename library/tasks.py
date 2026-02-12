import logging
from datetime import date
from celery import shared_task, group
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def send_mail_for_overdue_books(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        due_date = loan.due_date
        
        logger.info("Sending mail")
        
        
        send_mail(
            subject='Your Loan has been overdue.',
            message=f'Hello {loan.member.user.username},\n\nYour lend book: "{book_title}" has been passed the due date {due_date}.\nPlease return it as soon as possible.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass
    

@shared_task
def check_overdue_loans():
    try:
        today = date.today
        # get all the due date passed loans
        due_loans = Loan.objects.filter(
            is_returned=False,
            due_date__lt=date.today()
        ) 
        
        send_mails = group(send_mail_for_overdue_books.s(loan.id) for loan in due_loans)
        send_mails.apply_async()
        
    except Loan.DoesNotExist:
        pass
