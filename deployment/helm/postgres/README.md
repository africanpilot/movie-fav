# PostgreSQL Helm Chart

This Helm chart deploys PostgreSQL database with the same configurations as defined in the docker-compose-prod.yml file.

## Prerequisites

- Kubernetes 1.16+
- Helm 3.0+
- PV provisioner support in the underlying infrastructure (if persistence is enabled)

## Installing the Chart

To install the chart with the release name `my-postgres`:

```bash
helm install my-postgres ./postgres
```

The command deploys PostgreSQL on the Kubernetes cluster in the default configuration. The [Parameters](#parameters) section lists the parameters that can be configured during installation.

## Uninstalling the Chart

To uninstall/delete the `my-postgres` deployment:

```bash
helm delete my-postgres
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Parameters

### Global parameters

| Name                                      | Description                       | Value |
| ----------------------------------------- | --------------------------------- | ----- |
| `global.postgresql.auth.postgresPassword` | PostgreSQL postgres user password | `""`  |
| `global.postgresql.auth.username`         | PostgreSQL username               | `""`  |
| `global.postgresql.auth.password`         | PostgreSQL password               | `""`  |
| `global.postgresql.auth.database`         | PostgreSQL database name          | `""`  |

### Common parameters

| Name               | Description                                    | Value |
| ------------------ | ---------------------------------------------- | ----- |
| `nameOverride`     | String to partially override postgres.fullname | `""`  |
| `fullnameOverride` | String to fully override postgres.fullname     | `""`  |

### PostgreSQL Image parameters

| Name               | Description                  | Value          |
| ------------------ | ---------------------------- | -------------- |
| `image.repository` | PostgreSQL image repository  | `postgres`     |
| `image.tag`        | PostgreSQL image tag         | `15`           |
| `image.pullPolicy` | PostgreSQL image pull policy | `IfNotPresent` |

### PostgreSQL Authentication parameters

| Name                               | Description                            | Value      |
| ---------------------------------- | -------------------------------------- | ---------- |
| `postgresql.auth.postgresPassword` | Password for the "postgres" admin user | `password` |
| `postgresql.auth.username`         | Name for a custom user to create       | `postgres` |
| `postgresql.auth.password`         | Password for the custom user           | `password` |
| `postgresql.auth.database`         | Name for a custom database to create   | `postgres` |

### PostgreSQL Primary configuration parameters

| Name                       | Description                  | Value |
| -------------------------- | ---------------------------- | ----- |
| `postgresql.configuration` | PostgreSQL configuration     | `""`  |
| `postgresql.initdbScripts` | Dictionary of initdb scripts | `{}`  |

### PostgreSQL service parameters

| Name           | Description             | Value       |
| -------------- | ----------------------- | ----------- |
| `service.type` | PostgreSQL service type | `ClusterIP` |
| `service.port` | PostgreSQL service port | `5432`      |

### Persistence parameters

| Name                     | Description                               | Value           |
| ------------------------ | ----------------------------------------- | --------------- |
| `persistence.enabled`    | Enable PostgreSQL data persistence        | `true`          |
| `persistence.size`       | PVC Storage Request for PostgreSQL volume | `20Gi`          |
| `persistence.accessMode` | PVC Access Mode for PostgreSQL volume     | `ReadWriteOnce` |

### Resource parameters

| Name                        | Description                                       | Value   |
| --------------------------- | ------------------------------------------------- | ------- |
| `resources.limits.cpu`      | The resources limits for PostgreSQL containers    | `1000m` |
| `resources.limits.memory`   | The resources limits for PostgreSQL containers    | `1Gi`   |
| `resources.requests.cpu`    | The requested resources for PostgreSQL containers | `500m`  |
| `resources.requests.memory` | The requested resources for PostgreSQL containers | `512Mi` |

## Configuration and installation details

### Setting Pod's affinity

This chart allows you to set your custom affinity using the `affinity` parameter. Find more information about Pod's affinity in the [kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity).

### PostgreSQL configuration

PostgreSQL configuration can be specified via the `postgresql.configuration` parameter, which will be mounted at `/etc/postgresql/postgresql.conf`.

### Init scripts

You can specify dictionary of initdb scripts via the `postgresql.initdbScripts` parameter. The scripts will be mounted at `/docker-entrypoint-initdb.d` and executed during database initialization.

Example:

```yaml
postgresql:
  initdbScripts:
    001-create_all_db.sql: |
      -- Your SQL initialization script here
      CREATE DATABASE myapp;
      CREATE USER myuser WITH PASSWORD 'mypass';
      GRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;
```

## Troubleshooting

### PostgreSQL pods fail to start

If PostgreSQL pods fail to start, check:

1. PersistentVolume provisioning (if persistence is enabled)
2. Resource limits and requests
3. Pod security context and file permissions
4. Configuration syntax in postgresql.configuration

### Connection issues

If you can't connect to PostgreSQL:

1. Verify the service is running: `kubectl get svc`
2. Check pod logs: `kubectl logs <postgres-pod-name>`
3. Verify network policies are not blocking connections
4. Ensure credentials are correct in the secret

For more troubleshooting, see the PostgreSQL documentation: https://www.postgresql.org/docs/
