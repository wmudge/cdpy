# -*- coding: utf-8 -*-
import array

from cdpy.common import CdpSdkBase, Squelch

ENTITLEMENT_DISABLED = "Operational Database not enabled on CDP Tenant"


class CdpyOpdb(CdpSdkBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def describe_database(self, name=None, env=None):
        return self.sdk.call(
            svc="opdb",
            func="describe_database",
            ret_field="databaseDetails",
            squelch=[
                Squelch("NOT_FOUND"),
                Squelch("INVALID_ARGUMENT"),
                Squelch("UNKNOWN"),
                Squelch(value="PATH_DISABLED", warning=ENTITLEMENT_DISABLED),
            ],
            databaseName=name,
            environmentName=env,
        )

    def list_databases(self, env=None):
        return self.sdk.call(
            svc="opdb",
            func="list_databases",
            ret_field="databases",
            squelch=[
                Squelch(
                    value="NOT_FOUND",
                    default=list(),
                    warning="No OpDB Databases found in Tenant",
                ),
                Squelch(
                    value="PATH_DISABLED", default=list(), warning=ENTITLEMENT_DISABLED
                ),
            ],
            environmentName=env,
        )

    def describe_all_databases(self, env=None):
        ws_list = self.list_databases(env)
        resp = []
        for db in ws_list:
            db_desc = self.describe_database(db["databaseName"], db["environmentCrn"])
            if db_desc is not None:
                resp.append(db_desc)
        return resp

    def drop_database(self, name, env):
        return self.sdk.call(
            svc="opdb",
            func="drop_database",
            ret_field="status",
            squelch=[
                Squelch("NOT_FOUND"),
                Squelch(value="PATH_DISABLED", warning=ENTITLEMENT_DISABLED),
            ],
            databaseName=name,
            environmentName=env,
        )

    def create_database(
        self,
        name: str,
        env: str,
        attached_storage_for_workers: dict = None,
        auto_scaling_params: dict = None,
        compute_cluster_id: str = None,
        custom_user_tags: array = None,
        disable_external_db: bool = False,
        disable_jwt_auth: bool = False,
        disable_kerberos: bool = False,
        disable_multi_az: bool = False,
        enable_grafana: bool = False,
        enable_region_canary: bool = False,
        image: dict = None,
        java_version: int = None,
        num_edge_nodes: int = 0,
        recipes: list = None,
        root_volume_size: int = None,
        scale_type: str = None,
        storage_location: str = None,
        storage_type: str = None,
        subnet_id: str = None,
        volume_encryptions: list = None,
    ):
        return self.sdk.call(
            svc="opdb",
            func="create_database",
            ret_field="databaseDetails",
            squelch=[Squelch(value="PATH_DISABLED", warning=ENTITLEMENT_DISABLED)],
            databaseName=name,
            environmentName=env,
            attachedStorageForWorkers=attached_storage_for_workers,
            autoScalingParameters=auto_scaling_params,
            computeClusterId=compute_cluster_id,
            customUserTags=custom_user_tags,
            disableExternalDB=disable_external_db,
            disableJwtAuth=disable_jwt_auth,
            disableKerberos=disable_kerberos,
            disableMultiAz=disable_multi_az,
            enableGrafana=enable_grafana,
            enableRegionCanary=enable_region_canary,
            image=image,
            javaVersion=java_version,
            numEdgeNodes=num_edge_nodes,
            recipes=recipes,
            rootVolumeSize=root_volume_size,
            scaleType=scale_type,
            storageLocation=storage_location,
            storageType=storage_type,
            subnetId=subnet_id,
            volumeEncryptions=volume_encryptions,
        )

    def start_database(self, name, env):
        return self.sdk.call(
            svc="opdb",
            func="start_database",
            squelch=[
                Squelch("NOT_FOUND"),
                Squelch(value="PATH_DISABLED", warning=ENTITLEMENT_DISABLED),
            ],
            databaseName=name,
            environmentName=env,
        )

    def stop_database(self, name, env):
        return self.sdk.call(
            svc="opdb",
            func="stop_database",
            squelch=[
                Squelch("NOT_FOUND"),
                Squelch(value="PATH_DISABLED", warning=ENTITLEMENT_DISABLED),
            ],
            databaseName=name,
            environmentName=env,
        )
