
const { loadEnv, defineConfig } = require('@medusajs/framework/utils')

loadEnv(process.env.NODE_ENV || 'development', process.cwd())

module.exports = defineConfig({
    projectConfig: {
        databaseUrl: process.env.DATABASE_URL,
        // Esta línea es necesaria para compatibilidad con el core
        redisUrl: process.env.EVENTS_REDIS_URL,
        http: {
            storeCors: process.env.STORE_CORS!,
            adminCors: process.env.ADMIN_CORS!,
            authCors: process.env.AUTH_CORS!,
            jwtSecret: process.env.JWT_SECRET || 'supersecret',
            cookieSecret: process.env.COOKIE_SECRET || 'supersecret',
        },
    },
    admin: {
        disable: false,
        path: '/app',
    },
    modules: {
        // Módulo de eventos con Redis
        eventBus: {
            resolve: '@medusajs/event-bus-redis',
            options: {
                redisUrl: process.env.EVENTS_REDIS_URL,
                // Opciones recomendadas para producción
                jobOptions: {
                    removeOnComplete: {
                        age: 3600,
                        count: 1000,
                    },
                    removeOnFail: {
                        age: 3600,
                        count: 1000,
                    },
                },
            },
        },
        // Módulo de caché con Redis
        cacheModule: {
            resolve: '@medusajs/cache-redis',
            options: {
                redisUrl: process.env.CACHE_REDIS_URL,
                ttl: 60, // tiempo de vida de la caché en segundos (opcional)
            },
        },
        // (Opcional) Si luego necesitas workflow-engine, descomenta:
        // workflowEngine: {
        //   resolve: '@medusajs/workflow-engine-redis',
        //   options: {
        //     redis: {
        //       redisUrl: process.env.WE_REDIS_URL,
        //     },
        //   },
        // },
    },
})
