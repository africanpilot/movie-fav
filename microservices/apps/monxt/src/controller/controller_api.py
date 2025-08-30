# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_controller import ControllerToApollo
from link_models.enums import SchemaTypeEnum

class APIController(ControllerToApollo):
    """
    List of the class models for each query type.
    These classes must be in the ../api/ directories
    """
    
    public_models_to_load = [
      # account
      "AccountCreateMutation",
      "AccountConfirmEmailMutation",
      "AccountResendConfirmMutation",
      "AccountForgotPasswordMutation",
      "AccountForgotPasswordConfirmEmailMutation",
      "AccountAuthenticationLoginMutation",
      "AccountAuthenticationLogoutMutation",
      "AccountMeQuery",
      "AccountDeleteMutation",
      "AccountUpdateMutation",
      "AccountUpdatePasswordMutation",
      "AccountCompanyCreateMutation",
      "AccountCompanyUpdateMutation",
      "AccountCompanyQuery",
      "AccountGuestLoginMutation",
      "AccountAuthenticationAuthZeroLoginMutation",
      
      # cart
      "CartEventCreateMutation",
      "CartEventDeleteMutation",
      "CartEventUpdateMutation",
      "CartEventQuery",
      "CartProductCreateMutation",
      "CartProductDeleteMutation",
      "CartProductUpdateMutation",
      "CartProductQuery",
      "CartWishlistCreateMutation",
      "CartWishlistDeleteMutation",
      "CartWishlistUpdateMutation",
      "CartWishlistQuery",
      
      # collection
      "CollectionInfoCreateMutation",
      "CollectionInfoDeleteMutation",
      "CollectionInfoUpdateMutation",
      "CollectionInfoQuery",
      
      # event
      "EventInfoCreateMutation",
      "EventInfoDeleteMutation",
      "EventInfoUpdateMutation",
      "EventInfoQuery",
      "EventGeoQuery",
      "EventScheduleCreateMutation",
      "EventScheduleDeleteMutation",
      "EventScheduleUpdateMutation",
      "EventScheduleQuery",
      "EventTicketCreateMutation",
      "EventTicketDeleteMutation",
      "EventTicketUpdateMutation",
      "EventTicketQuery",
      "EventFederations",
      
      # movie
      "MovieInfoQuery",
      "MovieFederations",
      "MovieDownloadMutation",
      "MovieUpdateMutation",
      
      # notifications
      "NotificationsCreateMutation",
      "NotificationsCreateFormMutation",
      "NotificationsSagaStateQuery",
      "NotificationsUpdateMutation",
      
      # orders
      "OrdersInfoCreateMutation",
      "OrdersInfoUpdateMutation",
      "OrdersInfoQuery",
      "OrdersIntentCreateMutation",
      
      # person
      "PersonInfoQuery",
      "PersonFederations",
      
      # product
      "ProductInfoCreateMutation",
      "ProductInfoDeleteMutation",
      "ProductInfoUpdateMutation",
      "ProductInfoQuery",
      "ProductVariantCreateMutation",
      "ProductVariantDeleteMutation",
      "ProductVariantUpdateMutation",
      "ProductVariantQuery",
      "ProductCategoryQuery",
      "ProductColorQuery",
      "ProductFederations",
      "ProductSearchQuery",
      
      # shows
      "ShowsInfoQuery",
      "ShowsFederations",
      "ShowsEpisodeQuery",
      "ShowsDownloadMutation",
      "ShowsEpisodeUpdateMutation",
    ]
    
    private_models_to_load = [
      
      # movie
      "MovieInfoPopulateMutation",
      "MovieResetPopularMutation",
      "MovieRedisSyncMutation",
      "MovieImportMutation",
      "MovieInfoUpdateMutation",

      # orders
      "OrdersInfoDeleteMutation",
      
      # product
      "ProductIngestMutation",
      "ProductColorCreateMutation",
      
      # person
      "PersonInfoPopulateMutation",
      "PersonRedisSyncMutation",
      
      # shows
      "ShowsInfoPopulateMutation",
      "ShowsResetPopularMutation",
      "ShowsRedisSyncMutation",
      "ShowsInfoUpdateMutation",
    ]
    
    public_routes_to_load = [
      "LinkBaseRouter",
      
      # account
      "AccountAuthZeroRouter",
    ]

    private_routes_to_load = []

    def __init__(self, schema_type: SchemaTypeEnum = SchemaTypeEnum.PUBLIC, microservice: str = "monxt"):
        super().__init__(schema_type)
        self._schema_type = schema_type
        self._microservice = microservice

        self.set_models_to_load(self.public_models_to_load)
        
        if self._schema_type == SchemaTypeEnum.PRIVATE:
          self.set_models_to_load(self.private_models_to_load)


class APISchema:
  public_schema = APIController(schema_type=SchemaTypeEnum.PUBLIC).get_graphql_schema()
  private_schema = APIController(schema_type=SchemaTypeEnum.PRIVATE).get_graphql_schema()
  public_routes = APIController.public_routes_to_load
  private_routes = APIController.private_routes_to_load
