class ServiceLocator:
    __services = {}

    @staticmethod
    def register_service(service_name, service_instance):
        ServiceLocator.__services[service_name] = service_instance

    @staticmethod
    def get_service(service_name):
        return ServiceLocator.__services.get(service_name)
