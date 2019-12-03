from ranger.models import Ranger


def ranger_balance(request):
    try:
        ranger = Ranger.objects.get(user=request.user)
    except Ranger.DoesNotExist:
        return {}
    except:
        return {}
    else:
        return {"agent_balance": ranger.balance}
