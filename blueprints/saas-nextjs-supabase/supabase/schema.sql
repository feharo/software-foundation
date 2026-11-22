-- __APP_NAME__ SaaS starter schema.
-- Run once in Supabase SQL Editor. Test RLS with separate authenticated users.
-- Note: no invitations or billing in this starter. Memberships are owner-only.

begin;

create extension if not exists pgcrypto;

create table if not exists public.workspaces (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 3 and 80),
  owner_id uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists public.workspace_memberships (
  workspace_id uuid not null references public.workspaces(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null default 'member' check (role in ('owner','admin','member')),
  created_at timestamptz not null default now(),
  primary key(workspace_id, user_id)
);
create index if not exists memberships_user_idx on public.workspace_memberships(user_id, workspace_id);

create table if not exists public.tasks (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces(id) on delete cascade,
  created_by uuid not null references auth.users(id) on delete cascade,
  title text not null check (char_length(title) between 1 and 160),
  done boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists tasks_workspace_created_idx on public.tasks(workspace_id, created_at desc);

-- SECURITY DEFINER used only to check the caller's own membership.
-- All object references are fully qualified; no user-controlled search_path.
create or replace function public.is_workspace_member(target_workspace_id uuid)
returns boolean language sql stable security definer set search_path = ''
as $$
  select exists (
    select 1 from public.workspace_memberships as membership
    where membership.workspace_id = target_workspace_id
      and membership.user_id = (select auth.uid())
  );
$$;

-- When the authenticated owner creates a workspace, add own membership.
create or replace function public.add_workspace_owner()
returns trigger language plpgsql security definer set search_path = ''
as $$
begin
  insert into public.workspace_memberships(workspace_id, user_id, role)
  values (new.id, new.owner_id, 'owner')
  on conflict (workspace_id, user_id) do nothing;
  return new;
end;
$$;
drop trigger if exists workspaces_owner_membership on public.workspaces;
create trigger workspaces_owner_membership after insert on public.workspaces
for each row execute function public.add_workspace_owner();

alter table public.workspaces enable row level security;
alter table public.workspace_memberships enable row level security;
alter table public.tasks enable row level security;

-- Safe to re-run policies after a schema update.
drop policy if exists "workspace_select" on public.workspaces;
create policy "workspace_select" on public.workspaces
for select to authenticated
using (owner_id = (select auth.uid()) or public.is_workspace_member(id));

drop policy if exists "workspace_insert" on public.workspaces;
create policy "workspace_insert" on public.workspaces
for insert to authenticated
with check (owner_id = (select auth.uid()));

drop policy if exists "workspace_update" on public.workspaces;
create policy "workspace_update" on public.workspaces
for update to authenticated
using (owner_id = (select auth.uid()))
with check (owner_id = (select auth.uid()));

drop policy if exists "workspace_delete" on public.workspaces;
create policy "workspace_delete" on public.workspaces
for delete to authenticated
using (owner_id = (select auth.uid()));

drop policy if exists "member_select" on public.workspace_memberships;
create policy "member_select" on public.workspace_memberships
for select to authenticated using (user_id = (select auth.uid()));

-- No client grants for inserting/updating/deleting membership records.
-- Future team management must use an authorized backend/RPC with audit trail.

drop policy if exists "task_select" on public.tasks;
create policy "task_select" on public.tasks
for select to authenticated using (public.is_workspace_member(workspace_id));

drop policy if exists "task_insert" on public.tasks;
create policy "task_insert" on public.tasks
for insert to authenticated
with check (public.is_workspace_member(workspace_id) and created_by = (select auth.uid()));

drop policy if exists "task_update" on public.tasks;
create policy "task_update" on public.tasks
for update to authenticated
using (public.is_workspace_member(workspace_id))
with check (public.is_workspace_member(workspace_id) and created_by = (select auth.uid()));

drop policy if exists "task_delete" on public.tasks;
create policy "task_delete" on public.tasks
for delete to authenticated
using (public.is_workspace_member(workspace_id));

revoke all on public.workspaces, public.workspace_memberships, public.tasks from public, anon;
grant select, insert, update, delete on public.workspaces to authenticated;
grant select on public.workspace_memberships to authenticated;
grant select, insert, update, delete on public.tasks to authenticated;

revoke all on function public.is_workspace_member(uuid) from public, anon;
grant execute on function public.is_workspace_member(uuid) to authenticated;
revoke all on function public.add_workspace_owner() from public, anon;

commit;
