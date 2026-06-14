-- Core Restaurant Table
CREATE TABLE restaurants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    lat FLOAT,
    lng FLOAT,
    website TEXT,
    ig_handle TEXT,
    fb_page_id TEXT,
    confidence INT DEFAULT 0,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dishes and Menu Items
CREATE TABLE dishes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    price NUMERIC,
    description TEXT,
    category TEXT,
    tags TEXT[],
    image_url TEXT,
    image_source TEXT,
    image_confidence FLOAT,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Image Enrichment Cache
CREATE TABLE image_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_name TEXT NOT NULL UNIQUE,
    image_url TEXT NOT NULL,
    image_source TEXT,
    cached_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sync State for Change Detection
CREATE TABLE sync_state (
    restaurant_id UUID REFERENCES restaurants(id),
    source TEXT,
    content_hash TEXT,
    last_synced_at TIMESTAMPTZ,
    PRIMARY KEY (restaurant_id, source)
);

-- System Indexes
CREATE INDEX idx_dishes_restaurant ON dishes(restaurant_id);
CREATE INDEX idx_image_cache_name ON image_cache(item_name);
CREATE INDEX idx_dishes_tags ON dishes USING GIN(tags);