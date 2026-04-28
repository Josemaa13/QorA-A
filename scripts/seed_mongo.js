// Demo seed for QorA-A MongoDB (idempotent-ish)
// Usage:
// docker exec -i mongodb mongosh "mongodb://mongodb_user:mongodb_password@localhost:27017/admin?authSource=admin" < scripts/seed_mongo.js

const dbName = "qora_mongo";
const d = db.getSiblingDB(dbName);
const now = new Date();

// Clear previous seeded docs while preserving any other user-generated docs.
d.analytics.deleteMany({ source: "seed_demo_data" });
d.notifications.deleteMany({ source: "seed_demo_data" });
d.users.deleteMany({ source: "seed_demo_data" });
d.publications.deleteMany({ source: "seed_demo_data" });

d.users.insertMany([
  { username: "ana_data", email: "ana_data@qora.local", role: "data_engineer", source: "seed_demo_data", createdAt: now },
  { username: "carlos_ml", email: "carlos_ml@qora.local", role: "ml_engineer", source: "seed_demo_data", createdAt: now },
  { username: "lucia_bi", email: "lucia_bi@qora.local", role: "bi_analyst", source: "seed_demo_data", createdAt: now }
]);

d.publications.insertMany([
  { title: "Guia de Modelado de Datos", category: "Data Engineering", views: 124, source: "seed_demo_data", createdAt: now },
  { title: "Playbook de Entrenamiento ML", category: "Machine Learning", views: 97, source: "seed_demo_data", createdAt: now },
  { title: "Checklist de Calidad de Dashboards", category: "Business Intelligence", views: 76, source: "seed_demo_data", createdAt: now }
]);

const analytics = [];
for (let i = 0; i < 40; i += 1) {
  analytics.push({
    event_type: i % 3 === 0 ? "search_query" : "page_view",
    user_id: (i % 5) + 1,
    url_path: `/feed?page=${(i % 6) + 1}`,
    query: i % 3 === 0 ? "openmetadata lineage" : null,
    ip_address: `192.168.1.${20 + (i % 30)}`,
    timestamp: new Date(now.getTime() - i * 5 * 60 * 1000).toISOString(),
    source: "seed_demo_data"
  });
}
d.analytics.insertMany(analytics);

const notifications = [];
for (let i = 0; i < 20; i += 1) {
  notifications.push({
    recipient_id: (i % 4) + 1,
    actor_id: ((i + 1) % 5) + 1,
    verb: ["liked", "commented", "followed", "shared"][i % 4],
    target_id: (i % 4) + 1,
    target_type: "Document",
    is_read: i % 4 === 0,
    created_at: new Date(now.getTime() - i * 60 * 60 * 1000),
    source: "seed_demo_data"
  });
}
d.notifications.insertMany(notifications);

print(`Seed completed in MongoDB database: ${dbName}`);
print(`analytics=${d.analytics.countDocuments({})}`);
print(`notifications=${d.notifications.countDocuments({})}`);
print(`publications=${d.publications.countDocuments({})}`);
print(`users=${d.users.countDocuments({})}`);
