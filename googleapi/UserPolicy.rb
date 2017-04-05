#!/usr/bin/ruby
require 'set'
require 'aws-sdk'

def describe_user_policy(user,iam_client)
	user_policy_list = Set.new
	policies = iam_client.list_attached_user_policies({user_name: user})["attached_policies"]
	for policy in policies
		#puts policy["policy_name"]
		user_policy_list.add(policy["policy_name"])
	end
	groups_response = iam_client.list_groups_for_user(user_name:user).groups()
	user_groups_list = Array.new
	for groups in groups_response
		user_groups_list.push(groups.group_name)
	end
	puts "User Belongs to Groups"
	puts user_groups_list
	for group in user_groups_list
		response = iam_client.list_attached_group_policies({group_name: group}).attached_policies
		for policy in response
			user_policy_list.add(policy.policy_name)
		end
	end
	response = iam_client.list_user_policies({user_name: user}).policy_names
	if response.length() > 0
		puts "User: "+user+" Has inline polices"
		puts response.inspect
	end
	#user_policy_list.add("AdministratorAccess")
	user_policy_list.add("ReadOnlyAccess")
	user_policy_list = user_policy_list.to_a
	puts user
	puts user_policy_list.inspect
	return user_policy_list.to_a
end

def create_user_awsssorole(user,policy_list,iam_client)
	iam_role_name = "AWSSSORole_"+user
	command = "aws iam create-role --role-name #{iam_role_name} --assume-role-policy-document file:///Users/Achilles/sandbox/googleapi/rubycodes/trust.json"
	result =  `#{command}`
	if $?.exitstatus != 0
		 Kernel.abort("something went wrong in bash command for  #{command}")
	end
	puts "created IAM Role #{iam_role_name} for user: #{user}"
	for policy in policy_list
		policy_arn = "arn:aws:iam::aws:policy/#{policy}"
		begin
		iam_client.attach_role_policy({role_name: iam_role_name, policy_arn: policy_arn})
		puts "Attached AWS policy #{policy} to role #{iam_role_name}"
		rescue Exception => e
		policy_arn = "" #arn of iam policy
		iam_client.attach_role_policy({role_name: iam_role_name, policy_arn: policy_arn})
		puts "Attached Userdefined policy #{policy} to role #{iam_role_name}"
		end	
	end
end


def main()
	iam_client = iam = Aws::IAM::Client.new(region: "us-west-2")
	user_name = ['']
	#user_name = ['madhav'] 
	for user in user_name
		#user_policy_list = describe_user_policy(user,iam_client)
		user_policy_list =['AmazonEC2ReadOnlyAccess']
		create_user_awsssorole(user,user_policy_list,iam_client)
	end
end
main()
