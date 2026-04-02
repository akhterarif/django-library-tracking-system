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
def send_overdue_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        logger.info(loan)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned has been overdued',
            message=f'Hello {loan.member.user.username},\n\nYour book: "{book_title}" has been overdued.\nPlease return as soon as possible.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(
        is_returned=False,
        due_date__lt=date.today()
    )

    logger.info(overdue_loans)

    send_mails = group([send_overdue_notification.s(loan.id) for loan in overdue_loans])
    send_mails.apply_async()


    