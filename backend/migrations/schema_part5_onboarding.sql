-- ============================================================
-- Migration: onboarding flow support
-- Run: psql -U postgres -d engageai_db -f schema_part5_onboarding.sql
-- ============================================================

-- 1. organizations mein onboarding tracking flag
ALTER TABLE organizations
    ADD COLUMN onboarding_completed BOOLEAN NOT NULL DEFAULT FALSE;

-- 2. Signup ab sirf organization_name leta hai — baaki fields onboarding
--    wizard ke Tab 1 mein complete hote hain, isliye NOT NULL hata rahe hain.
ALTER TABLE organizations ALTER COLUMN business_type DROP NOT NULL;
ALTER TABLE organizations ALTER COLUMN website DROP NOT NULL;
ALTER TABLE organizations ALTER COLUMN business_email DROP NOT NULL;
ALTER TABLE organizations ALTER COLUMN business_phone DROP NOT NULL;
ALTER TABLE organizations ALTER COLUMN country DROP NOT NULL;

-- 3. representatives table already tumhare main SQL file mein ban chuki hai
--    (invitation flow ke sath) — koi change nahi. Yahan sirf confirm:
--    columns: representative_id, organization_id, representative_name,
--    service, service_description, company_email, invitation_token_hash,
--    invitation_expires_at, invitation_status, calendar_connected, status
