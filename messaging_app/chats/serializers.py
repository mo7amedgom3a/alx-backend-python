from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'bio', 'profile_picture', 
                 'phone_number', 'last_seen', 'is_online']
        read_only_fields = ['user_id', 'last_seen', 'is_online']

    def validate(self, data):
        """
        Validate that password and password_confirm match.
        """
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    message_body = serializers.CharField(required=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_id',
                 'message_body', 'sent_at', 'is_read', 'read_at']
        read_only_fields = ['message_id', 'sent_at', 'is_read', 'read_at']

    def validate_message_body(self, value):
        """
        Validate message body is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value.strip()


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model with nested relationships.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    title = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids',
                 'messages', 'created_at', 'updated_at', 'title', 'is_group']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.add(*participants)
            
            # Add the creator (current user) if they're not in the participant list
            if self.context['request'].user.user_id not in participant_ids:
                conversation.participants.add(self.context['request'].user)
        
        return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing conversations with last message.
    """
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'title', 'is_group',
                 'updated_at', 'last_message', 'unread_count']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()
