type Membership = {
  id: string;
  created_at: string;
  updated_at: string;
  partner_id: string;
  partner_name: string;
  menu_items: string[];
};

type UserInfo = {
  id: string;
  created_at: string;
  updated_at: string;
  name: string;
  email: string;
  memberships: Membership[];
};

export type User = {
  id: string;
  created_at: string;
  updated_at: string;
  access_token: string;
  user: UserInfo;
};
