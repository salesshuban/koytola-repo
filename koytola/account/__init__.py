class AccountEvents:
    """The different account event types."""

    # Account related events
    ACCOUNT_CREATED = "account_created"
    ACCOUNT_DELETED = "account_deleted"
    ACCOUNT_UPDATED = "account_updated"
    PASSWORD_RESET_LINK_SENT = "password_reset_link_sent"
    PASSWORD_RESET = "password_reset"
    PASSWORD_CHANGED = "password_changed"
    EMAIL_CHANGE_REQUEST = "email_changed_request"
    EMAIL_CHANGED = "email_changed"

    # Staff actions over accounts events
    ACCOUNT_ACTIVATED_BY_STAFF = "account_activated_by_staff"  # staff user activated an account
    ACCOUNT_DEACTIVATED_BY_STAFF = "account_deactivated_by_staff"  # staff user deactivated an account
    ACCOUNT_CREATED_BY_STAFF = "account_created_by_staff"  # staff user created an account
    ACCOUNT_DELETED_BY_STAFF = "account_deleted_by_staff"  # staff user deleted an account
    EMAIL_ASSIGNED_BY_STAFF = "email_assigned_by_staff"  # the staff user assigned an email to the account
    EMAIL_UPDATED_BY_STAFF = "email_updated_by_staff"  # the staff user updated an email of the account
    NAME_ASSIGNED_BY_STAFF = "name_assigned_by_staff"  # the staff user added set a name to the account
    NOTE_ADDED_BY_STAFF = "note_added_by_staff"  # the staff user added a note to the account
    NOTE_ADDED_TO_ORDER_BY_STAFF = "note_added_to_order_by_staff"  # the staff user added a note to an order

    # Order related events
    PLACED_ORDER = "placed_order"  # created an order
    ORDER_UPDATE = "order_update"
    NOTE_ADDED_TO_ORDER = "note_added_to_order"  # added a note to one of their orders
    DIGITAL_LINK_DOWNLOADED = "digital_link_downloaded"  # downloaded a digital good

    # Profile related events
    PROFILE_CREATED = "profile_created"
    PROFILE_UPDATED = "profile_updated"
    PROFILE_DELETED = "profile_deleted"
    PROFILE_CREATED_BY_STAFF = "profile_created_by_staff"
    PROFILE_UPDATED_BY_STAFF = "profile_updated_by_staff"
    PROFILE_DELETED_BY_STAFF = "profile_deleted_by_staff"
    PROFILE_ACTIVATED_BY_STAFF = "profile_activated_by_staff"
    PROFILE_DEACTIVATED_BY_STAFF = "profile_deactivated_by_staff"

    # Product related events
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"
    PRODUCT_CREATED_BY_STAFF = "product_created_by_staff"
    PRODUCT_UPDATED_BY_STAFF = "product_updated_by_staff"
    PRODUCT_DELETED_BY_STAFF = "product_deleted_by_staff"
    PRODUCT_ACTIVATED_BY_STAFF = "product_activated_by_staff"
    PRODUCT_DEACTIVATED_BY_STAFF = "product_deactivated_by_staff"

    CHOICES = [
        (ACCOUNT_CREATED, "The account was created"),
        (ACCOUNT_DELETED, "A account was deleted"),
        (ACCOUNT_UPDATED, "A account was updated"),
        (PASSWORD_RESET_LINK_SENT, "Password reset link was sent to the account"),
        (PASSWORD_RESET, "The account password was reset"),
        (EMAIL_CHANGE_REQUEST, "The user requested to change the account's email address."),
        (PASSWORD_CHANGED, "The account password was changed"),
        (EMAIL_CHANGED, "The account email address was changed"),

        (ACCOUNT_ACTIVATED_BY_STAFF, "Account was activated by staff member"),
        (ACCOUNT_DEACTIVATED_BY_STAFF, "Account was deactivated by staff member"),
        (ACCOUNT_CREATED_BY_STAFF, "Account was created by staff member"),
        (ACCOUNT_DELETED_BY_STAFF, "Account was deleted by staff member"),
        (EMAIL_ASSIGNED_BY_STAFF, "Email assigned to an account by staff member"),
        (EMAIL_UPDATED_BY_STAFF, "Email of an account updated by staff member"),
        (NAME_ASSIGNED_BY_STAFF, "Name assigned to an account by staff member"),
        (NOTE_ADDED_BY_STAFF, "Note added to an account by staff member"),

        (PLACED_ORDER, "An order was placed"),
        (ORDER_UPDATE, "An order was processed"),
        (NOTE_ADDED_TO_ORDER, "A note was added to order"),
        (DIGITAL_LINK_DOWNLOADED, "A digital good was downloaded"),

        (PROFILE_CREATED, "Profile was created"),
        (PROFILE_UPDATED, "Profile was updated"),
        (PROFILE_DELETED, "Profile was deleted"),
        (PROFILE_CREATED_BY_STAFF, "Profile was created by staff member"),
        (PROFILE_UPDATED_BY_STAFF, "Profile was updated by staff member"),
        (PROFILE_DELETED_BY_STAFF, "Profile was deleted by staff member"),
        (PROFILE_ACTIVATED_BY_STAFF, "Profile was activated by staff member"),
        (PROFILE_DEACTIVATED_BY_STAFF, "Profile was deactivated by staff member"),

        (PRODUCT_CREATED, "Product was created"),
        (PRODUCT_UPDATED, "Product was updated"),
        (PRODUCT_DELETED, "Product was deleted"),
        (PRODUCT_CREATED_BY_STAFF, "Product was created by staff member"),
        (PRODUCT_UPDATED_BY_STAFF, "Product was updated by staff member"),
        (PRODUCT_DELETED_BY_STAFF, "Product was deleted by staff member"),
        (PRODUCT_ACTIVATED_BY_STAFF, "Product was activated by staff member"),
        (PRODUCT_DEACTIVATED_BY_STAFF, "Product was deactivated by staff member"),
    ]
